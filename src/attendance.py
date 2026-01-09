import pandas as pd
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "..", "attendance")
CSV_FILE = os.path.join(FOLDER, "attendance.csv")
EXCEL_FILE = os.path.join(FOLDER, "attendance.xlsx")

def mark_attendance(name):
    os.makedirs(FOLDER, exist_ok=True)

    today = datetime.now().strftime("%d-%m-%Y")
    now = datetime.now().strftime("%H:%M:%S")

    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
        except:
            df = pd.DataFrame(columns=["Name", "Date", "Time"])
    else:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    if list(df.columns) != ["Name", "Date", "Time"]:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    duplicate = ((df["Name"] == name) & (df["Date"] == today)).any()

    if not duplicate:
        df.loc[len(df)] = [name, today, now]
        df.to_csv(CSV_FILE, index=False)
        df.to_excel(EXCEL_FILE, index=False)
        print("Attendance saved:", name)
        return True
    else:
        print("Already marked today:", name)
        return False
