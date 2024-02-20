from confluent_kafka import Producer
import time
import random
from datetime import datetime
import threading

class KafkaAlertsDataGenerator:

    def __init__(self):
        self.topic = "streaming.alerts.input"

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def run(self):
        try:
            print("Starting Kafka Alerts Generator..")
            # Wait for the main flow to be setup.
            time.sleep(5)

            # Setup Kafka Client
            conf = {'bootstrap.servers': "localhost:9092"}

            producer = Producer(**conf)

            # Define list of Exception Levels
            levels = ["CRITICAL", "HIGH", "ELEVATED"]

            # Define list of exception codes
            codes = ["100", "200", "300", "400"]

            # Define a random number generator
            random_gen = random.Random()

            # Create a record key using the system timestamp.
            rec_key = int(time.time())

            # Generate 100 sample exception messages
            for i in range(100):
                rec_key += 1

                # Capture current timestamp
                curr_time_stamp = datetime.now()
                # Get a random Exception Level
                this_level = random.choice(levels)
                # Get a random Exception code
                this_code = random.choice(codes)

                # Form a CSV. Use a dummy exception message
                value = f'"{curr_time_stamp}", "{this_level}", "{this_code}", "This is a {this_level} alert "'

                # Create the producer record and send data to Kafka
                producer.produce(self.topic, key=str(rec_key), value=value, callback=self.delivery_report)

                # Trigger any available delivery report callbacks from previous produce() calls
                producer.poll(0)

                print(f"Sending Event: {value}")

                # Wait for a random time (1 - 3 secs) before the next record.
                time.sleep(random_gen.randint(1, 3))

            # Wait for all messages to be delivered
            producer.flush()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    kodg = KafkaAlertsDataGenerator()
    threading.Thread(target=kodg.run).start()
