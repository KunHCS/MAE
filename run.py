"""
Runs the main program
"""
from multi_archive_extractor.utils import enqueue, extract_pass, process_output
from multi_archive_extractor.extractor import mp_extraction
import argparse


def main():
    parser = argparse.ArgumentParser(description='MAE')
    parser.add_argument('-r', '--rename', action='store_true',
                        help='prefix original archive')
    parser.add_argument('-p', '--password', type=str, default='pwd.txt',
                        help='optional password text file', metavar='')
    parser.add_argument('-e', '--extract', type=str, required=True,
                        help='file/directory to extract', metavar='')
    args = parser.parse_args()

    file_queue = enqueue([args.extract])
    # print(file_queue)
    pwd = extract_pass(args.password)
    print(pwd)
    output = mp_extraction(file_queue, args.rename, pwd)
    process_output(output)


if __name__ == "__main__":
    main()
