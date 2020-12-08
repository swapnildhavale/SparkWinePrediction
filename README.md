# SparkWinePrediction
Training Ramdom Forest model in EMR cluster.
Deploying the model in docker.(docker pull swappy7/cloudwinepred:v3)

1.	Create EMR Cluster.
https://us-east-2.console.aws.amazon.com/elasticmapreduce/home?region=us-east-2#quick-create:

2.	Update Security group of Master.
Under Inbound add new rule type: SSH and source: Anywhere.

3.	Now copy all the files including RFModelTrainer.py ValidationDataset.csv and TrainingDataset.cvs into EMR.
sftp -i ~/Desktop/Jars/frstEc2.pem hadoop@ec2-18-218-239-94.us-east-2.compute.amazonaws.com

put RFModelTrainer.py and similarly remaining two file in EMR.

4.	Now login into the cluster using following:
ssh -i frstEc2.pem hadoop@ec2-18-218-239-94.us-east-2.compute.amazonaws.com

5.	Now all your files will be in home/Hadoop.
You need to send or place files in Hadoop file system (fs) for parallel execution using following command.

hadoop fs -put TrainingDataset.csv /user/hadoop/TrainingDataset.csv

hadoop fs -put ValidationDataset.csv
/user/hadoop/ ValidationDataset.csv

6.	Once all the files are placed in fs we can start the execution by using following command:
RUN spark-submit RFModelTrainer.py

7.	Our Model is saved in Hadoop file system in order to copy it locally we need to use following command
hdfs dfs -copyToLocal ModelV1 /home/hadoop/

8.	Now we finally have our ModelV1. Copy the model (ModelV1) to our local machine.

9.	Create a container using docker following files are required:

10.	Now run following command to build a docker
docker build -t cloudwinepred .
docker tag 8ec0a32ca8bf swappy7/cloudwinepred:v3
docker push swappy7/cloudwinepred

11.	Now Image is pushed on docker hub.

12.	Fetch the image using:
docker pull swappy7/cloudwinepred:v3

13.	In order to run use 

docker run -v ~/Desktop/TestDataset.csv:/app/TestDataset.csv swappy7/cloudwinepred:v3

~/Desktop/TestDataset.csv is the file location local system.

14.	Run Docker in EC2 instance:
1.	Create a EC2 instance 

2.	Copy the TestDataset.csv into EC2 /home/ec2-user using following command:
scp -i ~/Desktop/Jars/frstEc2.pem ~/Desktop/TestDataset.csv ec2-user@ec2-13-58-212-106.us-east-2.compute.amazonaws.com:/home/ec2-user

3.	Use ssh -i ~/Desktop/Jars/frstEc2.pem ec2-user@ec2-13-58-212-106.us-east-2.compute.amazonaws.com to access EC2.

4.	In EC2 install docker use following command:
sudo yum update -y
sudo yum install docker -y
sudo service docker start

5.	sudo docker pull swappy7/cloudwinepred:v3 to pull the Image.

6.	sudo docker run -v /home/ec2-user/TestDataset.csv:/app/TestDataset.csv swappy7/cloudwinepred:v3

You will get F1-score and Accuracy
######
FOR MORE DETAILS REGARDING THE EXECUTION AND TRAINING OF MODEL PLEASE REFER Readme.doc
