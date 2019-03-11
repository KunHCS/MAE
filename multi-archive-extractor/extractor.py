"""
Handles extraction for multiple archives
"""
from subprocess import Popen
import subprocess
from sys import argv
from collections import deque
from pathlib import Path
from shutil import rmtree

Q = deque()
FORMATS = ('.zip', '.rar')
PASSWORDS = list()


def enqueue(arg_list):
    for path in arg_list:
        if Path(path).is_dir():
            enqueue([i for i in Path(path).iterdir()])
        elif Path(path).is_file() and str(path).endswith(FORMATS):
            Q.append(str(path))


def extract(archive):
    success = False
    for pwd in PASSWORDS:
        if success:
            break
        command = f'7z x {archive} -p{pwd} -y -o{archive.split(".")[-2]}'
        p = Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()
        if p.returncode == 0:
            success = True

    # deleted empty directory
    if not success:
        rmtree(archive.split(".")[-2], ignore_errors=True)

    return success


def extract_pass():
    try:
        with open('pwd.txt', 'r', encoding='UTF-8') as file:
            PASSWORDS.extend(file.read().splitlines())
            return True
    except FileNotFoundError:
        with open('pwd.txt', 'w+', encoding='UTF-8'):
            return False


def main():
    enqueue(argv[1:])
    if not extract_pass():
        print('No password file found')
        return -1
    print(PASSWORDS)
    success_count = 0
    for file in Q:
        success = extract(file)
        if success:
            success_count += 1
            print(f'{file} Extracted Successfully')
        else:
            print(f'{file} Failed to Extract')
    print(f'{success_count} out of {len(Q)} Extracted')


if __name__ == "__main__":
    main()
