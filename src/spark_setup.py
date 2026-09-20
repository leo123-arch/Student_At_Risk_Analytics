from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("StudentAcademicAnalytics") \
    .master("local[*]") \
    .getOrCreate()

print("Spark started successfully!")
print("Spark version:", spark.version)

spark.stop()