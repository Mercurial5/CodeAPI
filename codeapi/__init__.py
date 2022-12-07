from codeapi.languages import Language
from codeapi.utils import StringTools
from codeapi.utils import FileManager
from codeapi.executors import Docker


def check(lang: str, code: str, weak_inputs: list, weak_outputs: list, strong_inputs: list, strong_outputs: list,
          case_time: float) -> dict:
    if len(weak_inputs) != len(weak_outputs) or len(strong_inputs) != len(strong_outputs):
        raise ValueError('Wrong length of inputs and outputs')

    language = Language.get_language_by_name(lang)

    docker = Docker(language.name)

    file_manager = FileManager(language.path)

    result = check_weak_cases(language, code, file_manager, docker, weak_inputs, weak_outputs)
    if not result['status']:
        return result

    if len(strong_inputs) == 0:
        return result

    # Building new code with template to check a lot of cases with one run
    code = StringTools.build_template(template_name=language.name, timeout_seconds=case_time, code=code,
                                      iterations_number=len(strong_inputs))

    return check_strong_cases(language, code, file_manager, docker, strong_inputs, strong_outputs, len(weak_inputs))


def check_weak_cases(language: Language, code: str, file_manager: FileManager, docker: Docker, inputs: list,
                     outputs: list) -> dict:
    filename = file_manager.create_file(content=code, extension=language.extension)

    container_path_to_file = file_manager.join(docker.path_to_container_volume, language.name, filename)
    for index, (input_case, output_case) in enumerate(zip(inputs, outputs), start=1):
        docker.run(language.run(container_path_to_file))
        stdout, stderr = docker.communicate(input_case)

        result = None
        if stderr == 'Timeout':
            result = dict(status=False, reason='TL', case=index)
        elif stderr:
            result = dict(status=False, reason='RE', description=stderr)

        if stdout != output_case:
            result = dict(status=False, reason='WA', case=index)

        if result is not None:
            file_manager.delete_file(filename)
            return result

    file_manager.delete_file(filename)

    return dict(status=True)


def check_strong_cases(language: Language, code: str, file_manager: FileManager, docker: Docker, inputs: list,
                       outputs: list, case_shift: int) -> dict:
    filename = file_manager.create_file(code, extension=language.extension)
    container_path_to_file = file_manager.join(docker.path_to_container_volume, language.name, filename)
    docker.run(language.run(container_path_to_file))

    stdout, stderr = docker.communicate('\n'.join(inputs), 10)
    file_manager.delete_file(filename)

    if stderr:
        return dict(status=False, reason=stdout, description=stderr)

    user_outputs = StringTools.parse_outputs(stdout)
    for index, (output_user, output_answer) in enumerate(zip(user_outputs, outputs), start=1):
        if output_user['status']:
            if output_user['answer'] != output_answer:
                return dict(status=False, reason='WA', case=case_shift + index)
        else:
            return dict(status=False, reason=output_user['error'], case=case_shift + index)

    return dict(status=True)
