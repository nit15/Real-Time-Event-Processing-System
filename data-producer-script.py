from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v:json.dumps(v).encode('utf-8'))

while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {"sensor_id":random.randint(1,10), "value":random.uniform(10.0,100.0), "timestamp":current_time}
    producer.send('sensor-data', data)
    print(f"Sent: {data}")
    time.sleep(1)

# Database set-up
# Download and install postgres, select postgres services such as pgadmin for windows to run the server on port 5432 by default.
# add PATH to the PATH variable of SYSTEM_VARIABLES in Environment_variables-advance settings "C:\Program Files\PostgreSQL\17\bin" So that psql can be accessed from anywhere in the system.
# In psql by default postgres username[postgres] and enter the password you set up on the time of installation.
# create database in postgres database, create table and it's attributes.
# make change in postgresql.conf file, listeners:"*" instead of "localhost".
# make change in pg_hba.conf add:
# host    all             all             0.0.0.0/0               md5
# at the end of the file.
# if firewall blocks connection sometimes then please add rule in Windows firewall protection on PORT 5432, Allow every connection, domain.
