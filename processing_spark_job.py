# from pyspark.sql import SparkSession
#
# # Kafka topic and bootstrap server
# kafka_topic = "sensor-data"
# kafka_bootstrap_servers = "kafka:29092"  # Use 'kafka' for inter-container communication
#
# # Create Spark session
# spark = SparkSession.builder \
#     .appName("KafkaIntegration") \
#     .master("spark://spark-master:7077")\
#     .getOrCreate()
#
# # Read data from Kafka
# kafka_df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#     .option("subscribe", kafka_topic) \
#     .load()
#
# # Write data to console
# kafka_df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start() \
#     .awaitTermination()

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

# Define the schema of your JSON data
schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("value", FloatType(), True),
    StructField("timestamp", StringType(), True)
])

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Kafka to PostgreSQL") \
    .getOrCreate()

# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "sensor-data") \
    .load()

# Deserialize JSON data
deserialized_df = kafka_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select(
    col("data.sensor_id"),
    col("data.value"),
    to_timestamp(col("data.timestamp"), "yyyy-MM-dd HH:mm:ss").alias("timestamp")  # Convert to TimestampType
)

# Write to PostgreSQL
deserialized_df.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda batch_df, _: batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5432/sensor_db") \
        .option("dbtable", "sensor_table") \
        .option("user", "postgres") \
        .option("password", "153200") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append")\
        .save()) \
    .start() \
    .awaitTermination()


# Run this in terminal to Run the spark_job

# Make sure topic is created on kafka and the service is running successfully on docker container.
# 1) docker cp processing_spark_job.py spark-master:/opt/bitnami/spark/processing_spark_job.py
# 2) docker exec - it spark-master /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 \
#              --deploy-mode client \
#              --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,org.apache.kafka:kafka-clients:3.4.1,org.postgresql:postgresql:42.6.0 \
#              --conf "spark.executor.extraClassPath=/opt/bitnami/spark/.ivy2/jars/*" \
#              --conf "spark.driver.extraClassPath=/opt/bitnami/spark/.ivy2/jars/*" \
#              /opt/bitnami/spark/processing_spark_job.py

