import os
import random
import tempfile
from lib.zipfile import ZipFile
from lib.timer import timer
import time
import concurrent.futures


@timer
def unzip_ThreadPoolExecutor(file, dest):
    def unzip_member(zf, member, dest):
        zf.extract(member, dest)
        file = os.path.join(dest, member.filename)

    with open(file, 'rb') as f:
        zf = ZipFile(f)
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for member in zf.infolist():
                futures.append(
                    executor.submit(
                        unzip_member,
                        zf,
                        member,
                        dest,
                    )
                )

def _unzip_member_f3(zip_filepath, filename, dest):
    with open(zip_filepath, 'rb') as f:
        zf = ZipFile(f)
        zf.extract(filename, dest)
    file = os.path.join(dest, filename)

@timer
def unzip_ProcessPoolExecutor(file, dest):
    with open(file, 'rb') as f:
        zf = ZipFile(f)
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for member in zf.infolist():
                futures.append(
                    executor.submit(
                        _unzip_member_f3,
                        file,
                        member.filename,
                        dest,
                    )
                )

def main():
    dir = os.getcwd() + str(os.sep)
    for file in os.listdir(dir):
        if '.zip' in file and file is not os.path.isdir(file):
            new_dir = os.path.splitext(file)[0]
            if os.path.isdir(new_dir):
                print('Folder of the file: \"{0}\" already exists'.format(file))
                continue
            size = os.path.getsize(file)/1024/1024 # size in Mbytes
            if size > 500.0:
                unzip_ProcessPoolExecutor(file, new_dir)
            else:
                unzip_ThreadPoolExecutor(file, new_dir)
    print('\nFinisched')
    time.sleep(2)

if __name__ == '__main__':
    main()
