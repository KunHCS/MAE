"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
import multiprocessing
import os
from pathlib import PurePath


def extract(archive, pwd_list=None):
    success = False
    out_path = os.path.splitext(archive)[0]
    for pwd in pwd_list:
        if success:
            break

        args = ['7z', 'x', archive, f'-p{pwd}', '-y', f'-o{out_path}']
        p = Popen(args, stderr=PIPE, stdout=PIPE)

        p.communicate()
        if p.returncode == 0:
            success = True

    file_name = PurePath(archive).name
    print(f'Success: {file_name}' if success else f'Failed:  {archive}')

    # deleted empty files and directory
    if not success:
        rmtree(out_path, ignore_errors=True)

    return success


def mp_extraction(file_queue, pwd):
    if not file_queue:
        print('No supported files')
        return
    map_args = [(file, pwd) for file in file_queue]
    with multiprocessing.Pool() as pool:
        output = pool.starmap(extract, map_args)
        success_count = 0
        for stat in output:
            if stat:
                success_count += 1
    print(f'\n{success_count} out of {len(file_queue)} succeeded')
