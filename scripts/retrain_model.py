import argparse
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from config.settings import MODEL_PATH


DATASET_COLUMNS = [
    "study_hours_per_day",
    "attendance_percentage",
    "mental_health_rating",
    "sleep_hours",
    "part_time_job",
    "exam_score",
]


def train_model(dataset_path: str, model_path: str = MODEL_PATH) -> dict:
    dataset = pd.read_csv(dataset_path)
    missing_columns = [column for column in DATASET_COLUMNS if column not in dataset]
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {', '.join(missing_columns)}"
        )

    training_data = dataset[DATASET_COLUMNS].copy()
    for column in DATASET_COLUMNS:
        if column != "part_time_job":
            training_data[column] = pd.to_numeric(
                training_data[column], errors="coerce"
            )

    job_status = training_data["part_time_job"].astype("string").str.strip().str.title()
    invalid_statuses = job_status.notna() & ~job_status.isin(["Yes", "No"])
    if invalid_statuses.any():
        raise ValueError("part_time_job values must be Yes or No.")
    training_data["part_time_job"] = job_status.map({"No": 0, "Yes": 1})

    valid_rows = training_data.notna().all(axis=1)
    dropped_rows = int((~valid_rows).sum())
    training_data = training_data.loc[valid_rows]
    if len(training_data) < 20:
        raise ValueError("At least 20 complete rows are required to train a model.")
    if ((training_data["exam_score"] < 0) | (training_data["exam_score"] > 100)).any():
        raise ValueError("exam_score values must be between 0 and 100.")

    features = training_data[
        [
            "study_hours_per_day",
            "attendance_percentage",
            "mental_health_rating",
            "sleep_hours",
            "part_time_job",
        ]
    ].rename(
        columns={
            "study_hours_per_day": "study_hours",
            "attendance_percentage": "attendance",
            "mental_health_rating": "mental_health",
        }
    )
    target = training_data["exam_score"]

    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    estimator = RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    estimator.fit(x_train, y_train)

    predicted = estimator.predict(x_test)
    metrics = {
        "rows": len(training_data),
        "dropped_rows": dropped_rows,
        "r2": float(r2_score(y_test, predicted)),
        "mae": float(mean_absolute_error(y_test, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predicted))),
    }

    output_path = Path(model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(estimator, output_path)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train the prediction model from an authorized CSV dataset."
    )
    parser.add_argument(
        "--dataset",
        default=os.environ.get("SIS_DATASET_PATH"),
        help="CSV path (or set SIS_DATASET_PATH).",
    )
    parser.add_argument("--output", default=MODEL_PATH, help="Model output path.")
    args = parser.parse_args()
    if not args.dataset:
        parser.error("provide --dataset or set SIS_DATASET_PATH")

    metrics = train_model(args.dataset, args.output)
    print(f"Training rows: {metrics['rows']}")
    print(f"Incomplete rows skipped: {metrics['dropped_rows']}")
    print(f"Holdout R²: {metrics['r2']:.4f}")
    print(f"Holdout MAE: {metrics['mae']:.2f} points")
    print(f"Holdout RMSE: {metrics['rmse']:.2f} points")
    print(f"Saved model to: {args.output}")


if __name__ == "__main__":
    main()
