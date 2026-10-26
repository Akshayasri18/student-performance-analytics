#!/bin/bash
# Usage: bash push_to_github.sh <your-github-username>
set -e
git init
git add students.csv functions.py main.py results.csv README.md screenshots
git commit -m "Student Performance Analytics System"
git branch -M main
git remote add origin https://github.com/$1/student-performance-analytics.git
git push -u origin main
