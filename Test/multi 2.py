from multiprocessing import Pool


class A:
    def __init__(self, njobs=1000):
        self.map = Pool().map
        self.njobs = njobs
        self.start()

    def start(self):
        self.result = self.map(self.RunProcess, range(self.njobs))
        return self.result

    def RunProcess(self, i):
        return i * i


myA = A()
