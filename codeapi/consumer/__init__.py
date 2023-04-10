import json

from codeapi import check
from codeapi.config import RabbitMQ
from codeapi.database import Verdict, PostgresDatabase


def process_code(body: dict) -> dict:
    lang = body.get('lang')
    code = body.get('code')
    weak_inputs = body.get('weak_inputs')
    weak_outputs = body.get('weak_outputs')
    strong_inputs = body.get('strong_inputs', [])
    strong_outputs = body.get('strong_outputs', [])
    case_time = body.get('case_time')

    if None in (lang, code, weak_inputs, weak_outputs, strong_inputs, strong_outputs, case_time):
        return dict(status=False, reason='Not all data was given')

    try:
        case_time = float(case_time)
    except TypeError:
        return dict(status=False, reason='case_time should be float')

    try:
        return check(lang, code, weak_inputs, weak_outputs, strong_inputs, strong_outputs, case_time)
    except ValueError as e:
        return dict(status=False, reason='error', error=str(e))


def save_result(task_id: str, result: dict) -> None:
    verdict = Verdict(task_id=task_id, data=result)

    with PostgresDatabase() as database:
        database.session.add(verdict)
        database.session.commit()


def callback(ch, method, properties, body):
    body: dict = json.loads(body)
    task_id = body.pop('task_id')
    result = process_code(body)
    save_result(task_id, result)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start():
    connection = RabbitMQ.get_connection()
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='code-api-queue', auto_ack=False, on_message_callback=callback)
    channel.start_consuming()
