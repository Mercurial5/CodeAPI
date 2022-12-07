import os


class StringTools:
    """
    Class that manages +- complex string operations. Here
    """

    @staticmethod
    def build_template(template_name: str, code: str, iterations_number: int, timeout_seconds: float) -> str:
        with open(f'codeapi/templates/{template_name}', 'r') as file:
            template = file.read()

        code = template.format(iterations_number=iterations_number,
                               case_time=timeout_seconds,
                               code='        '.join(code.splitlines(True)),
                               case_delimiter=os.getenv('CASE_DELIMITER'),
                               timeout_error_message=os.getenv('TIMEOUT_ERROR_MESSAGE'))

        return code

    @staticmethod
    def parse_outputs(outputs: str) -> list:
        outputs: list = outputs.split(os.getenv('CASE_DELIMITER'))[:-1]
        outputs = [output.strip() for output in outputs]

        for index, output in enumerate(outputs):
            if output == os.getenv('TIMEOUT_ERROR_MESSAGE'):
                outputs[index] = dict(status=False, error='TL')
            else:
                outputs[index] = dict(status=True, answer=output)

        return outputs
