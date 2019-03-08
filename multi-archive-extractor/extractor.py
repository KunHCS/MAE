"""
Handles extraction for multiple archives
"""
from subprocess import Popen
from sys import argv
from collections import deque
from pathlib import Path, PurePosixPath, PosixPath

Q = deque()
FORMATS = ('.zip', '.rar')


def enqueue(arg_list):
    for path in arg_list:
        if Path(path).is_dir():
            enqueue([i for i in Path(path).iterdir()])
        elif Path(path).is_file() and str(path).endswith(FORMATS):
            Q.append(str(path))


def extract(archive):
    command = f'7z x {archive} -pr4 -y -o{archive.split(".")[-2]}'
    p = Popen(command)
    # print(p.stdout)


def main():
    enqueue(argv)
    for file in Q:
        extract(file)


if __name__ == "__main__":
    main()
    print(Q)
    print(len(Q))
