import csv
import random

random.seed(42)

departments = ["Computer", "IT", "AI"]

with open("data/students_large.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "student_id",
        "gender",
        "department",
        "attendance",
        "internal_marks",
        "assignment_score",
        "previous_cgpa",
        "backlogs",
        "study_hours",
        "at_risk"
    ])

    for i in range(1, 50001):

        student_id = f"S{i:05d}"
        gender = random.choice(["Male", "Female"])
        department = random.choice(departments)

        # Decide whether this student belongs to the
        # high-risk or normal student group.
        high_risk = random.random() < 0.20

        if high_risk:

            attendance = random.randint(45, 70)
            internal_marks = random.randint(35, 65)
            assignment_score = random.randint(35, 70)
            previous_cgpa = round(random.uniform(4.8, 6.8), 2)
            backlogs = random.randint(1, 3)
            study_hours = round(random.uniform(1, 4), 1)

            at_risk = 1

        else:

            attendance = random.randint(65, 100)
            internal_marks = random.randint(55, 100)
            assignment_score = random.randint(55, 100)
            previous_cgpa = round(random.uniform(6.5, 10.0), 2)
            backlogs = random.choice([0, 0, 0, 1])
            study_hours = round(random.uniform(3, 8), 1)

            at_risk = 0

        writer.writerow([
            student_id,
            gender,
            department,
            attendance,
            internal_marks,
            assignment_score,
            previous_cgpa,
            backlogs,
            study_hours,
            at_risk
        ])

print("50,000 realistic student records generated successfully!")