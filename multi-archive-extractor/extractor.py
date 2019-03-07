"""
Handles extraction for multiple archives
"""
import subprocess
from pathlib import Path


def extract():
    command = '7z x'
    file_name = 'r4.rar'
    file_path = Path(f'D:/Work/test/{file_name}')

    # TODO: Use regex instead
    out_dir = Path(f'-oD:/Work/test/{file_name.split(".")[0]}')

    print(out_dir)
    print(file_path)
    # argument for calling 7z
    args = command + file_path + out_dir
    print(args)
    # p = subprocess.Popen(args)
    return


def main():
    extract()


if __name__ == "__main__":
    main()
