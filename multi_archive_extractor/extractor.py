"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
from .utils import shrink_dir
import multiprocessing
import os


def extract(archive=None, add_prefix=False, pwd_list=None, shrink=False):
    """
    Extracts an archive using 7z checking over a password list
    :param archive:
    :param add_prefix:
    :param pwd_list:
    :param shrink:
    :return:
    """
    success = False
    ignore = False
    prefix = 'zzz_'
    correct_pass = ''
    err = b''
    return_code = -1
    out_path = os.path.splitext(archive)[0]
    path_split = os.path.split(archive)
    file_name = path_split[1]

    print('Started: ', archive)
    if file_name.startswith(prefix):
        ignore = True
        success = True

    for pwd in pwd_list:
        if success:
            break

        args = ['7z', 'x', archive, f'-p{pwd}', '-y', f'-o{out_path}']
        with Popen(args, stderr=PIPE, stdout=PIPE) as p:
            _, err = p.communicate()
        return_code = p.returncode

        if return_code == 0:
            correct_pass = pwd
            success = True
    if success:
        if add_prefix and not file_name.startswith(prefix):
            os.rename(archive, os.path.join(path_split[0], prefix + file_name))

        if shrink:
            shrink_dir(out_path)
    else:
        rmtree(out_path, ignore_errors=True)
    try:
        fail_err = err.decode('utf-8')
    except UnicodeDecodeError as e:
        fail_err = str(e)
    result = {'success': success, 'file': file_name, 'ignored': ignore,
              'password': correct_pass, 'ret_code': return_code, 'error':
                  fail_err}
    print('Done: ', archive)
    return result


def mp_extraction(file_queue, pwd, has_prefix, shrink):
    """
    Extracts all archives in file_queue in parallel
    :param file_queue:
    :param pwd:
    :param has_prefix:
    :param shrink:
    :return:
    """
    if not file_queue:
        print('No supported files')
        return

    map_args = [(file, has_prefix, pwd, shrink) for file in file_queue]
    with multiprocessing.Pool() as pool:
        output = pool.starmap(extract, map_args)

    return output
