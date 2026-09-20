from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, sum

spark = SparkSession.builder \
    .appName("StudentAtRiskBDA") \
    .master("local[*]") \
    .getOrCreate()

# Load large dataset
df = spark.read.csv(
    "data/students_large.csv",
    header=True,
    inferSchema=True
)

print("\n===== DATASET INFORMATION =====")

print("Number of students:", df.count())

print("\n===== DATA SCHEMA =====")
df.printSchema()

print("\n===== FIRST 10 STUDENTS =====")
df.show(10)

# ------------------------------------------------
# Overall statistics
# ------------------------------------------------

print("\n===== OVERALL STATISTICS =====")

df.select(
    avg("attendance").alias("Average Attendance"),
    avg("internal_marks").alias("Average Internal Marks"),
    avg("assignment_score").alias("Average Assignment Score"),
    avg("previous_cgpa").alias("Average CGPA"),
    avg("study_hours").alias("Average Study Hours")
).show()

# ------------------------------------------------
# At-risk analysis
# ------------------------------------------------

print("\n===== AT-RISK ANALYSIS =====")

df.groupBy("at_risk").count().show()

# ------------------------------------------------
# Department analysis
# ------------------------------------------------

print("\n===== DEPARTMENT ANALYSIS =====")

df.groupBy("department").agg(
    count("*").alias("Students"),
    avg("attendance").alias("Average Attendance"),
    avg("internal_marks").alias("Average Internal Marks"),
    avg("previous_cgpa").alias("Average CGPA"),
    sum("at_risk").alias("At_Risk_Students")
).show()

spark.stop()