import csv
import os
from datetime import datetime

CSV_PATH = "attendance.csv"
HEADERS = ["Roll", "Login", "Logout", "Duration", "Type", "Date"]

TIME_FMT = "%d-%m-%Y %H:%M:%S"
DATE_FMT = "%d-%m-%Y"

def now_time():
    return datetime.now().strftime(TIME_FMT)

def today():
    return datetime.now().strftime(DATE_FMT)

def parse_time(s):
    try:
        return datetime.strptime(s, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return datetime.strptime(s, "%d-%m-%Y %H:%M")

def ensure_csv():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            csv.writer(f).writerow(HEADERS)

def mark_attendance(roll):
    ensure_csv()

    rows = []
    found = False
    now = now_time()

    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            rows.append(row)

    for r in rows:
        if r[0] == roll:
            found = True

            if r[2]:
                return "ALREADY"

            login = parse_time(r[1])
            logout = parse_time(now)
            diff = logout - login

            minutes = int(diff.total_seconds() // 60)
            hours = minutes / 60

            if hours < 1:
                status = "LESS"
            elif hours < 4:
                status = "HALF"
            else:
                status = "FULL"

            r[2] = now
            r[3] = f"{minutes}"
            r[4] = status
            r[5] = today()
            break

    if not found:
        rows.append([roll, now, "", "", "", today()])

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(rows)

    return "UPDATED" if found else "CREATED"