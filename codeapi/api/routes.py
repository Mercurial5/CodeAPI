from flask import request

from codeapi.api import app
from codeapi import check


@app.route('/run', methods=['POST'])
def run():
    language = request.json.get('language')
    code = request.json.get('code')
    weak_inputs = request.json.get('weak_inputs')
    weak_outputs = request.json.get('weak_outputs')
    strong_inputs = request.json.get('strong_inputs', [])
    strong_outputs = request.json.get('strong_outputs', [])
    case_time = request.json.get('case_time')

    print(request.json)

    if None in (language, code, weak_inputs, weak_outputs, strong_inputs, strong_outputs, case_time):
        return dict(status=False, reason='Not all data was given')

    try:
        case_time = float(case_time)
    except TypeError:
        return dict(status=False, reason='case_time should be float')

    try:
        return check(language, code, weak_inputs, weak_outputs, strong_inputs, strong_outputs, case_time)
    except ValueError as e:
        return dict(status=False, reason='error', error=str(e))