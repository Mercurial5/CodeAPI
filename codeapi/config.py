from os import environ

from dotenv import load_dotenv
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from sqlalchemy import URL

load_dotenv()


class RabbitMQ:
    HOST = environ['RABBITMQ_HOST']
    PORT = int(environ['RABBITMQ_PORT'])
    USERNAME = environ['RABBITMQ_USERNAME']
    PASSWORD = environ['RABBITMQ_PASSWORD']
    CONSUME_QUEUE = environ['RABBITMQ_CONSUME_QUEUE']

    @staticmethod
    def get_connection() -> BlockingConnection:
        return BlockingConnection(RabbitMQ._get_parameters())

    @staticmethod
    def _get_parameters() -> ConnectionParameters:
        return ConnectionParameters(host=RabbitMQ.HOST, port=RabbitMQ.PORT, credentials=RabbitMQ._get_credentials())

    @staticmethod
    def _get_credentials() -> PlainCredentials:
        return PlainCredentials(username=RabbitMQ.USERNAME, password=RabbitMQ.PASSWORD)


class PostgresConfig:
    HOST = environ['POSTGRES_HOST']
    PORT = int(environ['POSTGRES_PORT'])
    USERNAME = environ['POSTGRES_USERNAME']
    PASSWORD = environ['POSTGRES_PASSWORD']
    DATABASE = environ['POSTGRES_DATABASE']

    @staticmethod
    def get_connection() -> URL:
        return URL.create('postgresql+psycopg2', username=PostgresConfig.USERNAME, password=PostgresConfig.PASSWORD,
                          host=PostgresConfig.HOST, port=PostgresConfig.PORT, database=PostgresConfig.DATABASE)

    @staticmethod
    def get_connection_for_alembic() -> str:
        return f'postgresql+psycopg2://{PostgresConfig.USERNAME}:{PostgresConfig.PASSWORD}@{PostgresConfig.HOST}' \
               f':{PostgresConfig.PORT}/{PostgresConfig.DATABASE}'
