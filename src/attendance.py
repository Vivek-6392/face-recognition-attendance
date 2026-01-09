import pandas as pd
from datetime import datetime
import os

def mark_attendance(name):
    file = "../attendance/attendance.csv"

    if not os.path.exists(file):
        df = pd.DataFrame(columns=["Name", "Time"])
    else:
        df = pd.read_csv(file)

    if name not in df["Name"].values:
        now = datetime.now().strftime("%H:%M:%S")
        df.loc[len(df)] = [name, now]
        df.to_csv(file, index=False)
