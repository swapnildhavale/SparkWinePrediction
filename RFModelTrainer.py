from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.shell import spark
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import DoubleType

df=spark.read.format("csv").option("inferSchema", "true").option("header", "true").option("sep", ";")\
    .load("/Users/swapnildhavale/Desktop/Jars/TrainingDataset.csv")

df=df.toDF("c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","quality")
featureassembler=VectorAssembler(inputCols=["c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11"],
outputCol="Independent Features")

output=featureassembler.transform(df)

finalized_data=output.select("Independent Features","quality")
train_data,test_data=finalized_data.randomSplit([0.75,0.25])

mlr = RandomForestClassifier(featuresCol='Independent Features', labelCol="quality",numTrees=16)
mlrModel=mlr.fit(finalized_data)

####TEST WITH TRAINING DATA#####
pred_results=mlrModel.transform(test_data)
pred_results.select('Independent Features',"quality",'prediction').show(5)

pred=mlrModel.transform(test_data)
evaluator = MulticlassClassificationEvaluator(
    labelCol="quality", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(pred)
print('Accuracy of training_data_set:',accuracy)

#####LOAIDNG VALIDATION DATA ######
df=spark.read.format("csv").option("inferSchema", "true").option("header", "true").option("sep", ";")\
    .load("/Users/swapnildhavale/Desktop/Jars/ValidationDataset.csv")

df=df.toDF("c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","quality")
featureassembler=VectorAssembler(inputCols=["c1", "c2","c3","c4","c5","c6","c7","c8","c9","c10","c11"],
outputCol="Independent Features")
output=featureassembler.transform(df)


test_data=output.select("Independent Features","quality")

pred=mlrModel.transform(test_data)
evaluator = MulticlassClassificationEvaluator(
    labelCol="quality", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(pred)


updated_pred=pred.withColumn("quality", pred["quality"].cast(DoubleType()))
predictionAndLabels=updated_pred.select("prediction","quality").rdd
lrmetrics = MulticlassMetrics(predictionAndLabels)
f1=lrmetrics.weightedFMeasure()
print('Accuracy is:',accuracy)
print('F1 Score:', f1)

######SAVE THE MODEL####
try:
    mlrModel.save("/Users/swapnildhavale/Desktop/Jars/ModelV1")
    print('SAVED')
except:
    print('Model Already Exist ..Rename the model..')