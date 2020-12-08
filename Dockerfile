FROM python:3.8.0-buster

RUN apt-get update
RUN apt-get install default-jdk -y

RUN pip install pyspark
RUN pip install numpy

#COPY requirements.txt .
#RUN pip install -r requirements.txt

# Copy everything to /app and make that our working directory
COPY . /app
WORKDIR /app

CMD ["python", "RF.py"]



