from pathlib import Path

FORMATS = ('.zip', '.rar')


def enqueue(arg_list):
    Q = list()
    for path in arg_list:
        if Path(path).is_dir():
            Q.extend(enqueue([i for i in Path(path).iterdir() if Path(
                path).is_dir()]))
        elif Path(path).is_file() and str(path).endswith(FORMATS):
            Q.append(str(path))
    return Q


def extract_pass(pwd_file):
    print('Extracting pass')
    try:
        with open(pwd_file, 'r', encoding='UTF-8') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        with open('pwd.txt', 'w+', encoding='UTF-8'):
            return None

