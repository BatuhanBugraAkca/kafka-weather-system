import json
from kafka import KafkaConsumer

# --- Kafka Settings ---
# This is the address for our Kafka server.
KAFKA_SERVER = "localhost:9092"
# This is the topic where we get the alerts.
TOPIC_NAME = "alerts"

# We make a Kafka Consumer to listen for messages.
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="alert-service-group"
)

print("Alert Service is working... Waiting for data from Kafka...")

# --- Threshold Values ---
# This is the temperature for a hot alert.
TEMP_THRESHOLD = 30
# This is the word we look for to see if there is a storm.
STORM_KEYWORD = "storm"

for message in consumer:
    data = message.value
    print(f"[INFO] New data is here: {data}")

    temp = data.get("temperature")
    weather_desc = data.get("weather", "").lower()

    if temp is not None and temp > TEMP_THRESHOLD:
        print(f"⚠️ ALERT: Temperature is too high! {temp}°C")

    if STORM_KEYWORD in weather_desc:
        print(f"⛈️ ALERT: Storm warning! Weather is: {weather_desc}")