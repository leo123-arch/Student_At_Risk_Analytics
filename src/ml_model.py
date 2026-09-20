from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# ------------------------------------------------
# 1. Start Spark
# ------------------------------------------------

spark = SparkSession.builder \
    .appName("StudentAtRiskPrediction") \
    .master("local[*]") \
    .getOrCreate()

# ------------------------------------------------
# 2. Load dataset
# ------------------------------------------------

df = spark.read.csv(
    "data/students_large.csv",
    header=True,
    inferSchema=True
)

print("\n===== DATASET =====")
print("Total students:", df.count())

# ------------------------------------------------
# 3. Convert categorical columns into numbers
# ------------------------------------------------

department_indexer = StringIndexer(
    inputCol="department",
    outputCol="department_index"
)

gender_indexer = StringIndexer(
    inputCol="gender",
    outputCol="gender_index"
)

# ------------------------------------------------
# 4. Combine input columns into feature vector
# ------------------------------------------------

assembler = VectorAssembler(
    inputCols=[
        "gender_index",
        "department_index",
        "attendance",
        "internal_marks",
        "assignment_score",
        "previous_cgpa",
        "backlogs",
        "study_hours"
    ],
    outputCol="features"
)

# ------------------------------------------------
# 5. Create Logistic Regression model
# ------------------------------------------------

lr = LogisticRegression(
    featuresCol="features",
    labelCol="at_risk"
)

# ------------------------------------------------
# 6. Create ML Pipeline
# ------------------------------------------------

pipeline = Pipeline(stages=[
    department_indexer,
    gender_indexer,
    assembler,
    lr
])

# ------------------------------------------------
# 7. Split data into training and testing
# ------------------------------------------------

train_data, test_data = df.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("\n===== DATA SPLIT =====")
print("Training records:", train_data.count())
print("Testing records:", test_data.count())

# ------------------------------------------------
# 8. Train model
# ------------------------------------------------

print("\n===== TRAINING MODEL =====")

model = pipeline.fit(train_data)

print("Model training completed!")

# ------------------------------------------------
# 9. Make predictions
# ------------------------------------------------

predictions = model.transform(test_data)

print("\n===== SAMPLE PREDICTIONS =====")

predictions.select(
    "student_id",
    "attendance",
    "internal_marks",
    "previous_cgpa",
    "backlogs",
    "at_risk",
    "prediction"
).show(20)

# ------------------------------------------------
# 10. Evaluate model
# ------------------------------------------------

evaluator = MulticlassClassificationEvaluator(
    labelCol="at_risk",
    predictionCol="prediction",
    metricName="accuracy"
)

accuracy = evaluator.evaluate(predictions)

print("\n===== MODEL PERFORMANCE =====")
print("Accuracy:", round(accuracy, 4))

# ------------------------------------------------
# Precision
# ------------------------------------------------

precision_evaluator = MulticlassClassificationEvaluator(
    labelCol="at_risk",
    predictionCol="prediction",
    metricName="weightedPrecision"
)

precision = precision_evaluator.evaluate(predictions)


# ------------------------------------------------
# Recall
# ------------------------------------------------

recall_evaluator = MulticlassClassificationEvaluator(
    labelCol="at_risk",
    predictionCol="prediction",
    metricName="weightedRecall"
)

recall = recall_evaluator.evaluate(predictions)


# ------------------------------------------------
# F1 Score
# ------------------------------------------------

f1_evaluator = MulticlassClassificationEvaluator(
    labelCol="at_risk",
    predictionCol="prediction",
    metricName="f1"
)

f1 = f1_evaluator.evaluate(predictions)


print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))


# ------------------------------------------------
# Confusion Matrix
# ------------------------------------------------

print("\n===== CONFUSION MATRIX =====")

predictions.groupBy(
    "at_risk",
    "prediction"
).count().orderBy(
    "at_risk",
    "prediction"
).show()

# ------------------------------------------------
# Save predictions for Power BI
# ------------------------------------------------

# ------------------------------------------------
# Save predictions for Power BI
# ------------------------------------------------

print("\n===== SAVING PREDICTIONS =====")

result_df = predictions.select(
    "student_id",
    "gender",
    "department",
    "attendance",
    "internal_marks",
    "assignment_score",
    "previous_cgpa",
    "backlogs",
    "study_hours",
    "at_risk",
    "prediction"
)

# Convert only the test predictions to Pandas
result_pd = result_df.toPandas()

# Convert prediction to readable text
result_pd["prediction"] = result_pd["prediction"].map({
    0.0: "Not At Risk",
    1.0: "At Risk"
})

# Save as one CSV file
result_pd.to_csv(
    "output/student_predictions.csv",
    index=False
)

print("Predictions saved successfully!")
print("File: output/student_predictions.csv")
    


spark.stop()