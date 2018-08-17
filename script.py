import os
import time
from multiprocessing import Pool
from app import Parser, FOLDER_NAME


def main(file_name):
    print('Parse file: {}'.format(file_name))
    parser = Parser(file_name)
    parser.start()


if __name__ == '__main__':
    list_files = os.listdir(FOLDER_NAME)
    files = [file for file in list_files if file.endswith('.csv')]
    time1 = time.time()
    with Pool(4) as p:
        p.map(main, files)
    time2 = time.time()
    print('Finish time: {}'.format((time2 - time1)))
