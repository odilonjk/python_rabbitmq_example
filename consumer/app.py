import pika
import json
import psycopg2

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS person (id SERIAL, name VARCHAR(80), gender VARCHAR(6), age integer);"
INSERT_SQL = "INSERT INTO person (name, gender, age) VALUES (%s, %s, %s);"


def callback(ch, method, properties, body):
    """
    Method used to consume the message on queue.
    Each message consumed will be parsed into JSON and persisted.
    """
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Message received.")
    data = json.loads(body)
    persist(data)


def persist(data):
    """This method persists the new person into the database."""
    conn = psycopg2.connect(host="localhost", database="integration", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute(INSERT_SQL, (data["name"], data["gender"], data["age"]))
    conn.commit()
    cursor.close()


def create_table():
    """
    Method used to create the person table on database.
    If the table already exists, this method will do nothing.
    """
    conn = psycopg2.connect(host="localhost", database="integration", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="integration",
                      durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue="integration")

create_table()

print("The consumer application has been started.")
channel.start_consuming()
