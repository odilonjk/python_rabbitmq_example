# A basic example of RabbitMQ's usage

This project contains an example of how to implement a consumer and a publisher of the messages on RabbitMQ queues. It also persists the received data into a Postgres schema.
Basically the publisher will create a person for each new message and send it to the queue. Then the consumer will catch the next message on the queue, parse it to JSON and finally persist the received person into the database.

## How to use it

1. Have [RabbitMQ](https://www.rabbitmq.com/) running on your computer.
2. Have a database on [PostgreSQL](https://www.postgresql.org/) called **integration**. For the sake of the example, it also must be running on localhost with user and password: **postgres**
Don't worry about the table. The consumer application will handle it.
3. Clone this repository.
4. Start the app.py file in the folder called consumer: `python app.py`
5. Start the app.py file in the folder called publisher, passing as the argument how many messages you want to send: `python app.py 300`

Ps.: You can start how many publishers/consumers you want.
