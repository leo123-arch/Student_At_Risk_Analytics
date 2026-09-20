from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("StudentAcademicAnalytics") \
    .master("local[*]") \
    .getOrCreate()

# Load student dataset
df = spark.read.csv(
    "data/students.csv",
    header=True,
    inferSchema=True
)

print("\n===== STUDENT DATA =====")
df.show()

print("\n===== DATA TYPES =====")
df.printSchema()

print("\n===== NUMBER OF STUDENTS =====")
print(df.count())

spark.stop()