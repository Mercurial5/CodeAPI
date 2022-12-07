from codeapi.languages import Language
from codeapi.utils import StringTools
from codeapi.utils import FileManager
from codeapi.executors import Docker


def check(lang: str, code: str, weak_inputs: list, weak_outputs: list, strong_inputs: list,
          strong_outputs: list,
          case_time: float) -> dict:
    float(case_time)
    if len(weak_inputs) != len(weak_outputs) or len(strong_inputs) != len(strong_outputs):
        raise ValueError('Wrong length of inputs and outputs')

    language = Language.get_language_by_name(lang)

    docker = Docker(language.name)

    file_manager = FileManager(language.path)
    filename = file_manager.create_file(content=code, extension=language.extension)

    container_path_to_file = file_manager.join(docker.path_to_container_volume, language.name, filename)
    for index, (input_case, output_case) in enumerate(zip(weak_inputs, weak_outputs), start=1):
        docker.run(language.run(container_path_to_file))
        stdout, stderr = docker.communicate(input_case)

        if stderr == 'Timeout':
            return dict(status=False, reason='TL', case=index)
        elif stderr:
            return dict(status=False, reason='RE', description=stderr)

        if stdout != output_case:
            return dict(status=False, reason='WA', case=index)

    file_manager.delete_file(filename)

    # Building new code with template to check a lot of cases with one run
    code = StringTools.build_template(template_name=language.name, timeout_seconds=case_time, code=code, iterations_number=len(strong_inputs))

    filename = file_manager.create_file(code, extension=language.extension)
    container_path_to_file = file_manager.join(docker.path_to_container_volume, language.name, filename)
    docker.run(language.run(container_path_to_file))

    stdout, stderr = docker.communicate('\n'.join(strong_inputs), 10)
    file_manager.delete_file(filename)

    if stderr:
        return dict(status=False, reason=stdout, description=stderr)

    outputs = StringTools.parse_outputs(stdout)
    for index, (output_user, output_answer) in enumerate(zip(outputs, strong_outputs), start=1):
        if output_user['status']:
            if output_user != output_answer:
                return dict(status=False, reason='WA', case=len(weak_inputs) + index)
        else:
            return dict(status=False, reason=output_user['error'], case=len(weak_inputs) + index)

    return dict(status=True)
