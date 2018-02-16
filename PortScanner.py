# -*- coding: utf-8 -*-ew
import threading, socket, sys, cmd, os, Queue
from netaddr import *

# 得到一个队列
def GetQueue(list):
    PortQueue = Queue.Queue(65535)
    for p in list:
        PortQueue.put(p)
    return PortQueue


# 超时时间
Timeout = 3.0

# 线程锁
screenLock = threading.Semaphore(value=1)


def write_file(filename, data):
    with open(filename, 'a+') as f:
        f.write(data)


class ScanThread(threading.Thread):
    def __init__(self, scanIP):
        threading.Thread.__init__(self)
        self.IP = scanIP

    def Ping(self, Port):
        global screenLock, Timeout
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            sock.settimeout(Timeout)
            address = (self.IP, Port)
            sock.connect(address)
            # sock.send('hello\r\n')
            # results = sock.recv(100)
            screenLock.acquire()
            # print '[+]IP:%s %d/tcp open' % (self.IP, Port)
            write_file(self.IP, '[+]IP:%s %d/tcp open' % (self.IP, Port) + '\n')
            screenLock.release()
            sock.close()
        except:
            sock.close()


class ScanThreadSingle(ScanThread):
    def __init__(self, scanIP, SingleQueue):
        ScanThread.__init__(self, scanIP)
        self.SingleQueue = SingleQueue

    def run(self):
        while not self.SingleQueue.empty():
            p = self.SingleQueue.get()
            self.Ping(p)


class ScanThreadMulti(ScanThread):
    def __init__(self, scanIP, PortList):
        ScanThread.__init__(self, scanIP)
        self.List = PortList[:]

    def run(self):
        for p in self.List:
            self.Ping(p)
