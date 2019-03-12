"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
import multiprocessing
import os


def extract(archive, has_prefix=False, pwd_list=None):
    success = False
    ignore = False
    prefix = 'zzz_'
    correct_pass = ''
    return_code = -1
    out_path = os.path.splitext(archive)[0]
    path_split = os.path.split(archive)
    file_name = path_split[1]

    if file_name.startswith(prefix):
        ignore = True
        success = True

    for pwd in pwd_list:
        if success:
            break

        args = ['7z', 'x', archive, f'-p{pwd}', '-y', f'-o{out_path}']
        with Popen(args, stderr=PIPE, stdout=PIPE) as p:
            p.communicate()
            return_code = p.returncode

        if return_code == 0:
            correct_pass = pwd
            success = True

    if success:
        print('o', end='')
        if has_prefix and not file_name.startswith(prefix):
            os.rename(archive, os.path.join(path_split[0], prefix+file_name))
    else:
        print('x', end='')
        rmtree(out_path, ignore_errors=True)

    result = {'success': success, 'file': file_name, 'ignored': ignore,
              'password': correct_pass, 'ret_code': return_code}
    return result


def mp_extraction(file_queue, has_prefix, pwd):
    if not file_queue:
        print('No supported files')
        return

    map_args = [(file, has_prefix, pwd) for file in file_queue]
    with multiprocessing.Pool() as pool:
        output = pool.starmap(extract, map_args)

    return output

