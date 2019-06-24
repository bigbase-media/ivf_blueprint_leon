# -*- coding: utf-8 -*-

import threading
from time import ctime,sleep


class BPThread(threading.Thread):
    def __init__(self, func, *args, name=''):
        threading.Thread.__init__(self)
        self._name = name
        self._func = func
        self._args = args
        self._output = None

    def run(self):
        print("name : ", self._name, " is running")
        self._output = self._func(*self._args)

    def join(self, timeout=None):
        super(BPThread, self).join(timeout=timeout)
        return self._output

def BFFunc(userInput):
    print("???")
    sleep(5)
    return userInput+userInput


def test():
    userInputs = ["abc", 3, "77a", "1000"]
    threads = []
    for i, input in enumerate(userInputs):
        t = BPThread(BFFunc, input, name=str(i))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start();
    outputs = []
    for t in threads:
        output = t.join()
        outputs.append(output)
    print("now let me see the outputs")
    print(outputs)

if __name__=="__main__":
    test()


