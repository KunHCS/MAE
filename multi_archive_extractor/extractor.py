"""
Handles extraction for multiple archives
"""
from subprocess import Popen, PIPE
from shutil import rmtree
import multiprocessing
import os


def extract(archive, pwd_list=None, encoding='UTF-8'):
    success = False
    out_path = os.path.splitext(archive)[0]

    encodings = ('ascii',
                 'big5',
                 'big5hkscs',
                 'cp037',
                 'cp273',
                 'cp424',
                 'cp437',
                 'cp500',
                 'cp720',
                 'cp737',
                 'cp775',
                 'cp850',
                 'cp852',
                 'cp855',
                 'cp856',
                 'cp857',
                 'cp858',
                 'cp860',
                 'cp861',
                 'cp862',
                 'cp863',
                 'cp864',
                 'cp865',
                 'cp866',
                 'cp869',
                 'cp874',
                 'cp875',
                 'cp932',
                 'cp949',
                 'cp950',
                 'cp1006',
                 'cp1026',
                 'cp1125',
                 'cp1140',
                 'cp1250',
                 'cp1251',
                 'cp1252',
                 'cp1253',
                 'cp1254',
                 'cp1255',
                 'cp1256',
                 'cp1257',
                 'cp1258',
                 'cp65001',
                 'euc_jp',
                 'euc_jis_2004',
                 'euc_jisx0213',
                 'euc_kr',
                 'gb2312',
                 'gbk',
                 'gb18030',
                 'hz',
                 'iso2022_jp',
                 'iso2022_jp_1',
                 'iso2022_jp_2',
                 'iso2022_jp_2004',
                 'iso2022_jp_3',
                 'iso2022_jp_ext',
                 'iso2022_kr',
                 'latin_1',
                 'iso8859_2',
                 'iso8859_3',
                 'iso8859_4',
                 'iso8859_5',
                 'iso8859_6',
                 'iso8859_7',
                 'iso8859_8',
                 'iso8859_9',
                 'iso8859_10',
                 'iso8859_11',
                 'iso8859_13',
                 'iso8859_14',
                 'iso8859_15',
                 'iso8859_16',
                 'johab',
                 'koi8_r',
                 'koi8_t',
                 'koi8_u',
                 'kz1048',
                 'mac_cyrillic',
                 'mac_greek',
                 'mac_iceland',
                 'mac_latin2',
                 'mac_roman',
                 'mac_turkish',
                 'ptcp154',
                 'shift_jis',
                 'shift_jis_2004',
                 'shift_jisx0213',
                 'utf_32',
                 'utf_32_be',
                 'utf_32_le',
                 'utf_16',
                 'utf_16_be',
                 'utf_16_le',
                 'utf_7',
                 'utf_8',
                 'utf_8_sig')

    for pa in pwd_list:
        pwd = pa
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
