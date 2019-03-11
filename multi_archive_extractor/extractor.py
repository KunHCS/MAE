"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
import multiprocessing
import os


def extract(archive, pwd_list=None):
    success = False
    out_path = os.path.splitext(archive)[0]

    for pwd in pwd_list:
        if success:
            break
        command = f'7z x {archive} -p{pwd} -y -o{out_path}'
        p = Popen(command, stderr=PIPE, stdout=PIPE)

        p.communicate()
        if p.returncode == 0:
            success = True

    print(f'Success: {archive}' if success else f'Failed:  {archive}')

    # deleted empty files and directory
    if not success:
        rmtree(out_path, ignore_errors=True)

    return success


def mp_extraction(file_queue, pwd):
    map_args = [(file, pwd) for file in file_queue]
    with multiprocessing.Pool() as pool:
        output = pool.starmap(extract, map_args)
        success_count = 0
        for stat in output:
            if stat:
                success_count += 1
    print(f'\n{success_count} out of {len(file_queue)} succeeded')

