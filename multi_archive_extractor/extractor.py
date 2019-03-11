"""
Handles extraction for multiple archives
"""
from subprocess import Popen
import subprocess
from shutil import rmtree
import multiprocessing


def extract(archive, pwd_list=None):
    print('active ', archive)
    success = False
    for pwd in pwd_list:
        if success:
            break
        command = f'7z x {archive} -p{pwd} -y -o{archive.split(".")[-2]}'
        p = Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()
        if p.returncode == 0:
            success = True

    # deleted empty files and directory
    if not success:
        rmtree(archive.split(".")[-2], ignore_errors=True)

    return success


def mp_extraction(file_queue, pwd):
    print(pwd)
    print(file_queue)
    map_arg = [(file, pwd) for file in file_queue]
    with multiprocessing.Pool() as pool:
        pool.starmap(extract, map_arg)

