import pika
import os

# Retrieve the CloudAMQP URL from environment variables
url = os.getenv('CLOUDAMQP_URL')
params = pika.URLParameters(url)

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='user')

# Define the callback function
def callback(ch, method, properties, body):
    print(f"Received: {body}")

# Set up subscription on the queue
channel.basic_consume(queue='user', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

# Start consuming
channel.start_consuming()

# Close the channel
channel.close()
