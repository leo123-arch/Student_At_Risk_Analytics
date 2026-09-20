from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

spark = SparkSession.builder \
    .appName("StudentAcademicAnalytics") \
    .master("local[*]") \
    .getOrCreate()

# Load dataset
df = spark.read.csv(
    "data/students.csv",
    header=True,
    inferSchema=True
)

# -------------------------------
# 1. Basic statistics
# -------------------------------

print("\n===== BASIC STATISTICS =====")

# Create a temporary SQL view
df.createOrReplaceTempView("students")

print("\n===== SPARK SQL: LOW ATTENDANCE =====")

low_attendance = spark.sql("""
    SELECT student_id, department, attendance, previous_cgpa, backlogs
    FROM students
    WHERE attendance < 60
""")

low_attendance.show()


print("\n===== SPARK SQL: DEPARTMENT PERFORMANCE =====")

department_analysis = spark.sql("""
    SELECT
        department,
        COUNT(*) AS total_students,
        ROUND(AVG(attendance), 2) AS avg_attendance,
        ROUND(AVG(internal_marks), 2) AS avg_internal_marks,
        ROUND(AVG(previous_cgpa), 2) AS avg_cgpa
    FROM students
    GROUP BY department
    ORDER BY avg_cgpa DESC
""")

department_analysis.show()