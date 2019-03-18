"""
Parse user inputs, initiates main program
"""
from multi_archive_extractor.utils import enqueue, extract_pass, process_result
from multi_archive_extractor.extractor import mp_extraction
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description='MAE')
    parser.add_argument('-s', '--shrink', action='store_true',
                        help='shrink output directory tree if applicable')
    parser.add_argument('-r', '--rename', action='store_true',
                        help='prefix original archive with zzz_ upon '
                             'successful extraction')
    parser.add_argument('-p', '--password', type=str, default='pwd.txt',
                        help='[-p <file>.txt] optional password text '
                             'file, defaults to pwd.txt file in program root',
                        metavar='')
    parser.add_argument('-e', '--extract', type=str, required=True,
                        help='[-e <directory>/<file(s)>] specify file(s)'
                             '/directory to '
                             'extract', metavar='')
    args = parser.parse_args()

    file_queue = enqueue([args.extract])
    pwd = extract_pass(args.password)
    print(pwd)
    output = mp_extraction(file_queue, pwd, args.rename, args.shrink)
    process_result(output)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'Elapsed Time: {end - start:.2f} Seconds')

