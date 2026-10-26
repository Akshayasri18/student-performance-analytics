"""Student Performance Analytics System - main program.

Run with:  python main.py
"""

import pandas as pd
import functions as fn

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # Step 1: Read the data
    df = fn.load_data("students.csv")

    print_header("DATASET OVERVIEW")
    print("Number of records :", len(df))
    print("Columns           :", list(df.columns))
    print("\nFirst 5 records:")
    print(df.head())

    # Step 2: Process the data
    df = fn.calculate_total_and_average(df)
    df = fn.assign_grades(df)
    df = fn.assign_pass_fail(df)

    print_header("STUDENT REPORT (Total, Average, Grade, Result)")
    print(df[["StudentID", "Name", "Department", "Total", "Average",
              "Grade", "Result"]].to_string(index=False))

    # Step 3: Analysis
    stats = fn.class_statistics(df)
    print_header("CLASS PERFORMANCE")
    print(f"Highest average : {stats['highest_name']} ({stats['highest_avg']})")
    print(f"Lowest average  : {stats['lowest_name']} ({stats['lowest_avg']})")
    print(f"Class average   : {stats['class_average']}")

    passed, failed, pass_pct = fn.pass_fail_statistics(df)
    print_header("PASS / FAIL STATISTICS")
    print(f"Total students : {len(df)}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {failed}")
    print(f"Pass percentage: {pass_pct}%")

    print_header("GRADE DISTRIBUTION")
    print(df["Grade"].value_counts().sort_index().to_string())

    subject_df = fn.subject_analysis(df)
    print_header("SUBJECT-WISE PERFORMANCE")
    print(subject_df.to_string(index=False))
    best = subject_df.loc[subject_df["Average"].idxmax()]
    weakest = subject_df.loc[subject_df["Average"].idxmin()]
    print(f"\nBest subject   : {best['Subject']} (avg {best['Average']})")
    print(f"Weakest subject: {weakest['Subject']} (avg {weakest['Average']})")

    print_header("TOP 5 PERFORMING STUDENTS")
    print(fn.top_performers(df, 5).to_string(index=False))

    print_header("DEPARTMENT-WISE ANALYSIS")
    print(fn.department_analysis(df).to_string(index=False))

    print_header("LOW ATTENDANCE STUDENTS (below 75%)")
    low = fn.low_attendance_students(df)
    print(low.to_string(index=False) if not low.empty else "None")

    # Save the processed results
    df.to_csv("results.csv", index=False)
    print("\nProcessed results saved to results.csv")


if __name__ == "__main__":
    main()
