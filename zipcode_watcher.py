from kafka import KafkaConsumer, KafkaProducer
import json

# --- Kafka Settings ---
# This is the address for our Kafka server.
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
# This is the topic where we get the weather info.
WEATHER_TOPIC = 'weather'
# This is the topic where we send the alerts.
ALERTS_TOPIC = 'alerts'

# --- Watched Zipcodes ---
# This is our list of special zip codes we want to watch.
WATCHED_ZIPCODES = ['60601', '60602']

def main():
    # --- Consumer ---
    # We make a consumer. It will listen to the 'weather' topic.
    consumer = KafkaConsumer(
        WEATHER_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='zipcode-watcher-group'
    )

    # --- Producer ---
    # We make a producer. It will send messages to the 'alerts' topic.
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("Zipcode Watcher Service is working...")

    # --- Main Loop ---
    # We check all the messages coming from the consumer.
    for message in consumer:
        weather_data = message.value
        # We get the zip code from the message.
        zipcode = str(weather_data.get("zipcode", ""))

        # We check if the zip code is in our special list.
        if zipcode in WATCHED_ZIPCODES:
            print(f"[MATCH] Watched zipcode: {zipcode}, sending data to alerts topic...")
            # If it is, we send the data to the 'alerts' topic.
            producer.send(ALERTS_TOPIC, weather_data)
        else:
            print(f"[SKIP] Zipcode {zipcode} is not in the watched list.")

if __name__ == "__main__":
    main()