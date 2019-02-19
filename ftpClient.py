import time
from socket import *
import sys
import os


class FtpClient(object):
    def __init__(self, client):
        self.client = client

    def doList(self):
        # 向服务端发送请求
        self.client.send(b'L')
        # 接收反馈
        data = self.client.recv(1024).decode()
        if data == 'OK':
            while True:
                filename = self.client.recv(1024).decode()
                if filename == '##':
                    break
                print(filename)
        else:
            print(data)

    def doGet(self):
        filename = input('请输入要下载的文件名')
        message = 'G ' + filename
        self.client.send(message.encode())
        data = self.client.recv(1024).decode()
        if data == 'OK':
            f = open(filename, 'wb')
            while True:
                data = self.client.recv(1024)
                if data == '##'.encode():
                    break
                f.write(data)
            f.close()
            print('%s下载完成' % filename)
        else:
            print(data)

    def doPut(self):
        filename=input('请输入要上传的文件')
        filename2=filename.split('/')[-1]
        try:
            f=open(filename,'rb')
        except:
            print('没有这个文件')
        self.client.send(('P '+filename2).encode())
        data=self.client.recv(1024)
        if data==b'OK':
            #读文件，发送数据
            while True:
                data=f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.client.send(b'##')
                    break
                self.client.send(data)
            f.close()
            print('%s上传完成'%filename2)
        else:
            print('服务器有问题')



    def doExit(self):
        self.client.send(b'Q')
        sys.exit('谢谢使用')


def main():
    if len(sys.argv) < 3:
        print('参数错误')
        return
    ADDRESS = (sys.argv[1], int(sys.argv[2]))
    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect(ADDRESS)
    except Exception as e:
        print('连接服务器失败', e)
        return
    # 连接成功,进入界面
    while True:
        # 创建类对象
        clientObj = FtpClient(client)
        prompt = '''
                  ========我爱静静网盘========
                  ****   1.查看文件列表   ****
                  ****     2.下载文件    ****
                  ****     3.上传文件    ****
                  ****     4.退出网盘    ****
                  ========================='''
        print(prompt)
        cmt = input('请选择')
        if cmt.strip() in ['1', '2', '3', '4']:
            if cmt == '1':
                clientObj.doList()
            elif cmt == '2':
                clientObj.doGet()
            elif cmt == '3':
                clientObj.doPut()
            else:
                clientObj.doExit()
        else:
            print('请做出正确的选择')


if __name__ == '__main__':
    main()
