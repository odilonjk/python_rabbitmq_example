import pika
import json
import sys
import names
import random


print("Connecting to RabbitMQ...")
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="integration",
                      durable=True)


def send_person():
    """Method used to send a new person to messenger queue."""
    person = create_person_json()
    message = json.dumps(person)
    publish(message)


def create_person_json() -> dict:
    """
    This method returns a new person in JSON format.
    The age and gender are chosen randomly.
    The name is created using a third-party lib, based on the person gender.
    """
    age = random.randint(18, 90)
    gender = "female" if random.choice([True, False]) else "male"
    name = names.get_full_name(gender=gender)
    return {"name": name, "gender": gender, "age": age}


def publish(message: str):
    """Send the message to the queue."""
    channel.basic_publish(exchange="",
                          routing_key="integration",
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

total = int(sys.argv[1])  # Get the command-line argument.
print("{} persons will be integrated.".format(total))

[send_person() for i in range(total)]

connection.close()
