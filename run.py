from multi_archive_extractor.setup import enqueue, extract_pass
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
    mp_extraction(file_queue, args.rename, pwd)


if __name__ == "__main__":
    main()
