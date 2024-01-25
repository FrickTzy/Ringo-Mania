from threading import Thread
from time import sleep


class A:
    def __init__(self):
        self.list = []

    def do_something(self, index):
        sleep(0.1)
        self.list.append(index)

    def print_final(self):
        sleep(0.4)
        print(f"final: {self.list}")

    def run(self):
        for i in range(100):
            Thread(target=self.do_something, args=(i,)).start()
        self.print_final()


if __name__ == '__main__':
    a = A()
    a.run()
