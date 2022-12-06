from flask import request

from codeapi.api import app
from codeapi import check


@app.route('/run', methods=['POST'])
def run():
    lang = request.form.get('lang')
    code = request.form.get('code')
    weak_inputs = request.form.getlist('weak_inputs')
    weak_outputs = request.form.getlist('weak_outputs')
    strong_inputs = request.form.getlist('strong_inputs')
    strong_outputs = request.form.getlist('strong_outputs')

    try:
        result = check(lang, code, weak_inputs, weak_outputs, strong_inputs, strong_outputs)
        return result
    except ValueError as e:
        return dict(status=False, reason='error', error=str(e))

