import os
from multiprocessing import Pool
from app import Parser, FOLDER_NAME

def main(file_name):
    print("*******")
    parser = Parser(file_name)
    parser.start()

if __name__ == '__main__':
    list_files = os.listdir(FOLDER_NAME)
    with Pool(4) as p:
        p.map(main, list_files)
