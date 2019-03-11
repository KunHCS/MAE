from pathlib import Path

FORMATS = ('.zip', '.rar', '.7z')


def enqueue(arg_list):
    q = list()
    for path in arg_list:
        if Path(path).is_dir():
            q.extend(enqueue(i for i in Path(path).iterdir() if Path(
                path).is_dir()))
        elif Path(path).is_file() and str(path).endswith(FORMATS):
            q.append(str(path))
    return q


def extract_pass(pwd_file):
    try:
        with open(pwd_file, 'r', encoding='UTF-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        with open('pwd.txt', 'w+', encoding='UTF-8'):
            return list()

