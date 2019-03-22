"""
Utilities
"""
from pathlib import Path
from shutil import rmtree
import json
import os

FORMATS = ('.zip', '.rar', '.7z')


def enqueue(arg_list):
    """
    Enqueue all files recursively
    :param arg_list:
    :return:
    """
    q = list()
    for path in arg_list:
        if Path(path).is_dir():
            q.extend(enqueue(i for i in Path(path).iterdir() if Path(
                path).is_dir()))
        elif Path(path).is_file() and str(path).endswith(FORMATS):
            q.append(str(path))
    return q


def extract_pass(pwd_file):
    """
    Extract password from text file separated by new line
    :param pwd_file:
    :return:
    """
    try:
        with open(pwd_file, 'r', encoding='utf-8-sig') as file:
            return [''] + file.read().splitlines()

    except FileNotFoundError:
        with open('pwd.txt', 'x', encoding='UTF-8'):
            return list()


def process_result(output):
    """
    Process the result of the extraction
    :param output:
    :return:
    """
    if not output:
        return
    print('')
    success_count = 0
    success_msg = ''
    failed_msg = ''
    freq = dict()
    for info in output:
        if info['success']:
            suffix = f' ({info["password"]})' if info["password"] else ''
            success_msg += f'Success:{suffix} {info["file"]}\n' \
                if not info['ignored'] else f'Ignored: {info["file"]}\n'
            success_count += 1
        else:
            failed_msg += f'Failed (err {info["ret_code"]}): {info["file"]}\n'
            err = info['error'] if len(info['error'].splitlines()) < 2 else \
                ''.join(line+'\n' for line in info['error'].splitlines()[
                                              :3])+'......'
            failed_msg += f'Error Message:\n{err}\n\n'
        freq[info['password']] = freq.get(info['password'], 0) + 1
        freq.pop('', None)
    print('Passwords used:')
    print(json.dumps(freq, indent=4))
    print()
    print(success_msg)
    print(failed_msg)
    print(f'\n{success_count} out of {len(output)} succeeded')


def shrink_dir(out_path):
    """
    If the sub directory only has one directory, move it up a level
    recursively
    :param out_path:
    :return:
    """
    check = True
    new_path = out_path
    while check:
        subs = os.listdir(new_path)
        if len(subs) == 1 and \
                os.path.isdir(os.path.join(new_path, subs[0])):
            new_path = os.path.join(new_path, subs[0])
        else:
            check = False

    if new_path != out_path:
        suffix = ''
        count = 0
        retry = True
        while retry:
            try:
                os.rename(new_path, os.path.join(out_path, '..',
                                                 os.path.split(new_path)[
                                                     1] + f'{suffix}'))
            except FileExistsError:
                count += 1
                suffix = f'_{count}'
            else:
                retry = False
        rmtree(out_path, ignore_errors=True)

