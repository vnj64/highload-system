from cassandra.cluster import Cluster
import pika


def save_to_db(data):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH REPLICATION = 
        {'class' : 'SimpleStrategy', 'replication_factor' : 1}
        """
    )
    session.execute("USE my_keyspace")

    session.execute(
        """
        CREATE TABLE IF NOT EXISTS person_data (
            url text PRIMARY KEY,
            person_name text,
            html_code text
        )
        """
    )

    session.execute(
        """
        INSERT INTO person_data (url, person_name, html_code)
        VALUES (%s, %s, %s)
        """,
        (data['url'], data['person_name'], data['html_code'])
    )

    cluster.shutdown()


def callback(ch, method, properties, body):
    data = body.decode('utf-8').split('\n')
    parsed_data = {
        'url': data[0],
        'person_name': data[1],
        'html_code': data[2]
    }

    save_to_db(parsed_data)
    print(f"Data for {parsed_data['url']} saved to the database")


def receive_data_from_queue(queue_name='parsed_data_queue'):
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    receive_data_from_queue()
