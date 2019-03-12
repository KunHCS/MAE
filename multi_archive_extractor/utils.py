"""
Utilities
"""
from pathlib import Path
import json

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
        with open(pwd_file, 'r', encoding='utf-8-sig') as file:
            return [''] + file.read().splitlines()

    except FileNotFoundError:
        with open('pwd.txt', 'w+', encoding='UTF-8'):
            return list()


def process_output(output):
    print('')
    success_count = 0
    success_msg = ''
    failed_msg = ''
    freq = dict()
    for info in output:
        print(info['ret_code'], end=' ')
        if info['success']:
            success_msg += f'Success({info["password"]}): {info["file"]}\n' \
                if not info['ignored'] else f'Ignored: {info["file"]}\n'
            success_count += 1
        else:
            failed_msg += f'Failed:  {info["file"]}\n'
        freq[info['password']] = freq.get(info['password'], 0) + 1
        freq.pop('', None)
    print()
    print(json.dumps(freq, indent=4))
    print(success_msg)
    print(failed_msg)
    print(f'\n{success_count} out of {len(output)} succeeded')


