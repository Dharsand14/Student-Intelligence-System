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


FEATURE_COLUMNS = {
    "study_hours": ("study_hours", "study_hours_per_day"),
    "attendance": ("attendance", "attendance_percentage"),
    "mental_health": ("mental_health", "mental_health_rating"),
    "sleep_hours": ("sleep_hours",),
}
TARGET_COLUMNS = ("exam_scores", "exam_score")
TRAINING_COLUMNS = tuple(FEATURE_COLUMNS)


def _read_dataset(dataset_path: str) -> pd.DataFrame:
    path = Path(dataset_path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError("Dataset must be a CSV or Excel workbook.")


def _select_column(dataset: pd.DataFrame, aliases: tuple[str, ...], label: str) -> str:
    matches = [column for column in aliases if column in dataset.columns]
    if not matches:
        raise ValueError(
            f"Dataset is missing a column for {label}: {', '.join(aliases)}"
        )
    if len(matches) > 1:
        raise ValueError(
            f"Dataset has multiple columns for {label}: {', '.join(matches)}"
        )
    return matches[0]


def train_model(dataset_path: str, model_path: str = MODEL_PATH) -> dict:
    dataset = _read_dataset(dataset_path)
    source_columns = {
        name: _select_column(dataset, aliases, name)
        for name, aliases in FEATURE_COLUMNS.items()
    }
    target_column = _select_column(dataset, TARGET_COLUMNS, "exam score target")
    training_data = dataset[
        [*source_columns.values(), target_column]
    ].rename(columns={source: name for name, source in source_columns.items()})
    training_data = training_data.rename(columns={target_column: "exam_score"})
    for column in (*TRAINING_COLUMNS, "exam_score"):
        training_data[column] = pd.to_numeric(training_data[column], errors="coerce")

    valid_rows = training_data.notna().all(axis=1)
    dropped_rows = int((~valid_rows).sum())
    training_data = training_data.loc[valid_rows]
    if len(training_data) < 20:
        raise ValueError("At least 20 complete rows are required to train a model.")
    if ((training_data["exam_score"] < 0) | (training_data["exam_score"] > 100)).any():
        raise ValueError("exam_score values must be between 0 and 100.")

    features = training_data[list(TRAINING_COLUMNS)]
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
        description="Train the prediction model from an authorized CSV or Excel dataset."
    )
    parser.add_argument(
        "--dataset",
        default=os.environ.get("SIS_DATASET_PATH"),
        help="CSV or Excel workbook path (or set SIS_DATASET_PATH).",
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
