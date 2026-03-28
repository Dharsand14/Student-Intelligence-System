import pandas as pd
import os

# ⭐ Always use absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "..", "student_database.xlsx")


def save_prediction(data):

    df = pd.DataFrame([data])

    if os.path.exists(DB_FILE):

        old_df = pd.read_excel(DB_FILE, engine="openpyxl")

        # Remove wrong column if exists
        if "Prediction" in old_df.columns:
            old_df = old_df.drop(columns=["Prediction"])

        new_df = pd.concat([old_df, df], ignore_index=True)

        new_df.to_excel(DB_FILE, index=False)

        print("📊 New prediction saved to database ✅")

    else:

        df.to_excel(DB_FILE, index=False)

        print("📁 New database created and prediction saved ✅")

    return DB_FILE


def delete_last_record():

    if os.path.exists(DB_FILE):

        df = pd.read_excel(DB_FILE, engine="openpyxl")

        if not df.empty:
            df = df.iloc[:-1]
            df.to_excel(DB_FILE, index=False)

            print("🗑️ Last record deleted successfully ❌")
            return True

        else:
            print("⚠️ Database is empty")
            return False

    print("❗ Database file not found")
    return False


def clear_database():

    if os.path.exists(DB_FILE):

        # keep columns but remove rows
        df = pd.read_excel(DB_FILE, engine="openpyxl")
        df = df.iloc[0:0]

        df.to_excel(DB_FILE, index=False)

        print("💥 All records cleared from database 🗑️")
        return True

    print("❗ Database file not found")
    return False