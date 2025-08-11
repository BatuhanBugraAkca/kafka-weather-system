Weather Alert System with Kafka
What This Project Does
This project is a small system for a home task. It checks the weather and can send alerts. The system has three small programs that work together and use Kafka to talk to each other.




How the Programs Work

Weather Fetcher Service: This program gets weather data from a weather website.


Zipcode Watcher Service: This program watches specific zipcodes for weather changes.


Alert Service: This program makes alerts if the weather is not good, for example, if it's very hot.


How to Run It
You can run this project easily with Docker on your computer.



What you need

Docker: You must have Docker on your computer.


API Key: You need a free key from the OpenWeatherMap website.

Steps
Get the project: Clone this project to your computer.

Bash

git clone https://github.com/BatuhanBugraAkca/kafka-weather-system.git
cd kafka-weather-system
Make a settings file: Create a file named .env in the project folder. Put your API key and the zipcodes you want to watch in this file.

Kod snippet'i

OPENWEATHERMAP_API_KEY=your_api_key_here
WATCHED_ZIPCODES=90210,10001
ALERT_THRESHOLD_TEMP_C=30

Start the system: Use this command to start all the programs.

Bash

docker-compose up --build
How to See an Alert
You can see an alert message in the program logs. When the weather is very hot for a zipcode you chose, the 

Alert Service will write a message saying there is an alert.
