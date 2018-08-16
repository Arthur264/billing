import os
from multiprocessing import Process
from app import Parser, FOLDER_NAME

def main(file_name):
    parser = Parser(file_name)
    print("test", id(parse))
    # parser.start()

if __name__ == '__main__':
    list_files = os.listdir(FOLDER_NAME)
    # with Pool(4) as p:
    #     p.map(main, list_files)
    processes = []
    for m in list_files:
       p = Process(target=main, args=(m,))
       p.start()
       processes.append(p)

    for p in processes:
       p.join()
