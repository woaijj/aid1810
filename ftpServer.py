from socket import *
from threading import Thread
import sys
import os
import time

# 定义全局变量
ADDRESS = ('0.0.0.0', 8888)
fileDir = '/home/tarena/桌面/python/项目/ftp/ftpfiles/'


def doRequest(client):
    # 创建对象
    clientObj = FtpServer(client)
    while True:
        message = client.recv(1024).decode()
        msgList = message.split()
        if msgList[0] == 'L':
            clientObj.doList()
        elif msgList[0] == 'G':
            clientObj.doGet(msgList[-1])
        elif msgList[0] == 'P':
            clientObj.doPut(msgList[-1])
        else:
            clientObj.doExit()


class FtpServer(object):
    def __init__(self, client):
        self.client = client

    def doList(self):
        fileList = os.listdir(fileDir)
        if not fileList:
            self.client.send('文件库为空'.encode())
        else:
            self.client.send(b'OK')
            time.sleep(0.1)
            for file in fileList:
                if os.path.isfile(fileDir + file) and file[0] != '.':
                    self.client.send(file.encode())
                    time.sleep(0.1)
            self.client.send(b'##')

    def doGet(self, filename):
        try:
            f = open(fileDir + filename, 'rb')
        except Exception:
            self.client.send('此文件不存在'.encode())
            return
        # 文件正常打开
        self.client.send(b'OK')
        time.sleep(0.1)
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.client.send(b'##')
                break
            self.client.send(data)
        f.close()

    def doPut(self, filename):
        try:
            f = open(fileDir + filename, 'wb')
        except Exception:
            self.client.send('上传失败'.encode())
            return
        self.client.send(b'OK')
        while True:
            data = self.client.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    def doExit(self):
        sys.exit(0)


# 创建网络连接


def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(ADDRESS)
    server.listen(10)
    print('正在等待客户端连接')
    while True:
        try:
            client, addr = server.accept()
        except KeyboardInterrupt:
            sys.exit('服务端推出')
        except Exception as e:
            print(e)
            continue
        t = Thread(target=doRequest, args=(client,))
        # 设置守护线程
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
