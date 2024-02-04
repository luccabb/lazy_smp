import multiprocessing

from uci import start

def main():
    multiprocessing.freeze_support()
    start()

if __name__ == "__main__":
    main()
