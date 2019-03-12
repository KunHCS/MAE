"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
import multiprocessing
import os


def extract(archive, add_prefix=False, pwd_list=None):
    success = False
    ignore = False
    prefix = 'zzz_'
    correct_pass = ''
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
        p = Popen(args, stderr=PIPE, stdout=PIPE)
        p.communicate()
        if p.returncode == 0:
            correct_pass = pwd
            success = True

    # deleted empty files and directory from 7z
    if success:
        print('#', end='')
        if add_prefix and not file_name.startswith(prefix):
            os.rename(archive, os.path.join(path_split[0], prefix+file_name))
    else:
        print('x', end='')
        rmtree(out_path, ignore_errors=True)

    result = {'success': success, 'file': file_name, 'ignored': ignore,
              'password': correct_pass}
    return result


def mp_extraction(file_queue, prefix, pwd):
    if not file_queue:
        print('No supported files')
        return

    map_args = [(file, prefix, pwd) for file in file_queue]
    with multiprocessing.Pool() as pool:
        output = pool.starmap(extract, map_args)

    print('')
    success_count = 0
    success_msg = ''
    failed_msg = ''
    freq = dict()
    for info in output:
        if info['success']:
            success_msg += f'Success: {info["file"]}\n' if not info[
                'ignored'] else f'Ignored: {info["file"]}\n'
            success_count += 1
        else:
            failed_msg += f'Failed:  {info["file"]}\n'
        freq[info['password']] = freq.get(info['password'], 0) + 1
        freq.pop('', None)

    print(freq)
    print(success_msg)
    print(failed_msg)
    print(f'\n{success_count} out of {len(file_queue)} succeeded')
