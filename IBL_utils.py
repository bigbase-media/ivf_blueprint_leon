# -*- coding: utf-8 -*-

import random

def get_random(lst):
    i = random.randint(0, len(lst)-1)
    return lst[i]


def test():
    lst = "abcdegf"
    lst = ['a', '11', 'cc', '8888', '***']
    print(get_random(lst))

if __name__=="__main__":
    test()
