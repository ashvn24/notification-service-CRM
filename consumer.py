import pika
import os, json, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')

# Initialize Django
django.setup()

from service.models import Notification

# Retrieve the CloudAMQP URL from environment variables
url = os.getenv('CLOUDAMQP_URL')
params = pika.URLParameters(url)

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='notification')

# Define the callback function
def callback(ch, method, properties, body):
    print(f"Received in notification-service")
    data =json.loads(body)
    
    if properties.content_type == 'user-created':
        db = Notification.objects.create(
            title='user-created',
            message = data['email']
        )
        db.save()
        print('user-created')

# Set up subscription on the queue
channel.basic_consume(queue='notification', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

# Start consuming
channel.start_consuming()

# Close the channel
channel.close()
