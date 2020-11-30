from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.shell import spark
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import DoubleType

df=spark.read.format("csv").option("inferSchema", "true").option("header", "true").option("sep", ";")\
    .load("TestDataset.csv")

###RENAMING THE CLOUMNS###
df=df.toDF("c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","quality")
featureassembler=VectorAssembler(inputCols=["c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11"],
outputCol="Independent Features")
output=featureassembler.transform(df)

test_data=output.select("Independent Features","quality")

#### LOADING_MODEL AND EVALUATING MODEL#####
reg=RandomForestClassificationModel.load("ModelV1")
pred=reg.transform(test_data)

pred.select('Independent Features',"quality",'prediction').show(5)
evaluator = MulticlassClassificationEvaluator(
    labelCol="quality", predictionCol="prediction", metricName="accuracy")
Accuracy = evaluator.evaluate(pred)

updated_pred=pred.withColumn("quality", pred["quality"].cast(DoubleType()))
predictionAndLabels=updated_pred.select("prediction","quality").rdd
lrmetrics = MulticlassMetrics(predictionAndLabels)
f1=lrmetrics.weightedFMeasure()
##PRINTING THE FINAL RESULT##
print('Accuracy is:',Accuracy)
print('F1 Score:', f1)

