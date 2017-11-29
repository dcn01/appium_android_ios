from multiprocessing import Process
import os
import time


def timetask(times):
    time.sleep(times)
    print("process:" + str(os.getpid()) + "__")


if __name__ == '__main__':
    for num in range(0, 20):  # 迭代 0 到 20 之间的数字
        arg = num
        p = Process(target=timetask, args=(arg,))
        p.start()
        p.join()
