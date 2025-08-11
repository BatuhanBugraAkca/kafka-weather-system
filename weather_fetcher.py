import json
import time
import requests
from kafka import KafkaProducer

# --- Configuration ---
# This is my API key. Don't share it.
API_KEY = "0c565685b7619a01bc541902676741a0"
# We check the weather for this city.
CITY = "Chicago"
# This is the zip code for the place we want to watch.
ZIPCODE = "60601"
# This is the address for our Kafka server.
KAFKA_SERVER = "localhost:9092"
# This is the name of our topic. Like a chat room.
TOPIC_NAME = "weather"

# --- Kafka Producer ---
# We make a producer. It will send messages to Kafka.
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# --- Function to Get Weather Data ---
def fetch_weather():
    # This is the link for the weather API. We use our city and API key.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY},US&appid={API_KEY}&units=metric"
    # We ask the API for the weather.
    response = requests.get(url)
    # We get the data and make it readable.
    data = response.json()

    # We print the full API response for checking (debug).
    print("API Response:", data)

    # We check if the data is good. If no 'main' part, it's an error.
    if "main" not in data:
        raise ValueError(f"API response does not contain 'main'. Response: {data}")

    # We take the parts we need and put them in a dictionary.
    return {
        "city": CITY,
        "zipcode": ZIPCODE,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"]
    }

# --- Main Program ---
if __name__ == "__main__":
    # This loop runs forever.
    while True:
        try:
            # We get the weather info from our function.
            weather_data = fetch_weather()
            # We print the data before sending it to Kafka.
            print(f"Sending to Kafka: {weather_data}")
            # We send our data to the Kafka topic.
            producer.send(TOPIC_NAME, weather_data)
        except Exception as e:
            # If there is a problem, we print the error.
            print("Error:", e)
        # We wait 10 seconds before doing it again.
        time.sleep(10)