from multi_archive_extractor.setup import enqueue, extract_pass
from multi_archive_extractor.extractor import mp_extraction
from sys import argv


def main():
    file_queue = enqueue(argv[1:])
    pwd = extract_pass('pwd.txt')
    mp_extraction(file_queue, pwd)


if __name__ == "__main__":
    main()
