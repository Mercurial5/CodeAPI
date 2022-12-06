import os


class StringTools:
    """
    Class that manages +- complex string operations.
    """

    @staticmethod
    def build_template(template_name: str, code: str, iterations_number: int) -> str:
        with open(f'codeapi/templates/{template_name}', 'r') as file:
            template = file.read()

        code = template.format(iterations_number=iterations_number, code='    '.join(code.splitlines(True)),
                               case_delimeter=os.getenv('CASE_DELIMITER'))

        return code

    @staticmethod
    def parse_outputs(outputs: str) -> list:
        outputs = outputs.split('CASE_DELIMITER')
        outputs = [output.strip() for output in outputs]

        return outputs
