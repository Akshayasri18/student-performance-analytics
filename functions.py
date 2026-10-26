"""Reusable calculation and processing functions for the
Student Performance Analytics System."""

import numpy as np
import pandas as pd

# Subject columns used throughout the project
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]

# Grading rule: pass mark per subject and grade boundaries on average marks
PASS_MARK = 40


def load_data(file_path):
    """Read the student CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def calculate_total_and_average(df):
    """Add Total and Average columns using NumPy on the subject marks."""
    marks = df[SUBJECTS].to_numpy()          # 2D NumPy array of marks
    df["Total"] = np.sum(marks, axis=1)
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def get_grade(average):
    """Return a grade for a given average mark.

    90+ -> A+, 80-89 -> A, 70-79 -> B, 60-69 -> C, 50-59 -> D, <50 -> F
    """
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    return "F"


def assign_grades(df):
    """Assign a grade to every student using a loop."""
    grades = []
    for avg in df["Average"]:                # loop over each student's average
        grades.append(get_grade(avg))
    df["Grade"] = grades
    return df


def assign_pass_fail(df):
    """A student passes only if every subject mark is >= PASS_MARK."""
    results = []
    for _, row in df.iterrows():
        if all(row[subject] >= PASS_MARK for subject in SUBJECTS):
            results.append("Pass")
        else:
            results.append("Fail")
    df["Result"] = results
    return df


def class_statistics(df):
    """Return highest, lowest and average performance of the class."""
    highest = df.loc[df["Average"].idxmax()]
    lowest = df.loc[df["Average"].idxmin()]
    return {
        "highest_name": highest["Name"],
        "highest_avg": highest["Average"],
        "lowest_name": lowest["Name"],
        "lowest_avg": lowest["Average"],
        "class_average": round(float(np.mean(df["Average"])), 2),
    }


def pass_fail_statistics(df):
    """Return number of passed/failed students and pass percentage."""
    passed = int((df["Result"] == "Pass").sum())
    failed = int((df["Result"] == "Fail").sum())
    pass_percentage = round(passed / len(df) * 100, 2)
    return passed, failed, pass_percentage


def subject_analysis(df):
    """Return a DataFrame with average, max and min mark for each subject."""
    rows = []
    for subject in SUBJECTS:
        column = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(column)), 2),
            "Highest": int(np.max(column)),
            "Lowest": int(np.min(column)),
        })
    return pd.DataFrame(rows)


def top_performers(df, n=5):
    """Return the top n students ranked by average marks."""
    top = df.sort_values(by="Average", ascending=False).head(n)
    return top[["StudentID", "Name", "Department", "Total", "Average", "Grade"]]


def department_analysis(df):
    """Average marks and attendance for each department."""
    return (df.groupby("Department")[["Average", "Attendance"]]
              .mean().round(2).reset_index())


def low_attendance_students(df, limit=75):
    """Students whose attendance is below the given percentage."""
    return df[df["Attendance"] < limit][["StudentID", "Name", "Attendance"]]
