
import socket
import threading

userName = ""
userPwd = ""

class L2TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"连接到服务器 {self.host}:{self.port}")
        except Exception as e:
            print(f"连接失败: {e}")

    def send_data(self, message):
        try:
            self.client_socket.sendall(message.encode('utf-8'))
            print("数据发送成功")
        except Exception as e:
            print(f"发送数据失败: {e}")

    def receive_data(self, buffer_size=1024):
        try:
            data = self.client_socket.recv(buffer_size)
            print("数据接收成功")
            return data.decode('utf-8')
        except Exception as e:
            print(f"接收数据失败: {e}")
            return None

    def close(self):
        self.client_socket.close()
        print("连接已关闭")

    def contains_success_regex(self,message):
        if "成功" in message:
            return True
        else:
            return False

    #订阅个股
    def subStock(self,stock):
        self.send_data("DY2,"+userName+","+userPwd+","+stock)
        data = self.receive_data()
        return self.contains_success_regex(data)
     #取消订阅个股
    def delSubStock(self,stock):
        self.send_data("QXDY2,"+userName+","+userPwd+","+stock)
        data = self.receive_data()
        return self.contains_success_regex(data)

    #查询订阅个股列表
    def queryStock(self):
        self.send_data("CXDY2,"+userName+","+userPwd)
        data = self.receive_data()
        return data
    
    def loginStock(self):
        self.send_data("DL,"+userName+","+userPwd)
        data = self.receive_data()
        return data
        


def Receive_data_thread(sock,taskName):
    while True:
        try:
            data = sock.receive_data()
            if not data:
                break
            print(f"{taskName} Received: {data}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break        

server = "www.l2api.cn"

if __name__ == "__main__":
    # 创建客户端实例
    OrderClient = L2TCPClient(server, 18103)
    
    # 连接到服务器
    OrderClient.connect()

    print(OrderClient.loginStock())
    print(OrderClient.subStock("000001.SZ"))
    print(OrderClient.subStock("000002.SZ"))
    # 在新线程中处理接收数据
    thread1 = threading.Thread(target=Receive_data_thread, args=(OrderClient,"Order"))
    thread1.start()
    
    #假如盘中修改订阅请使用第二个Socket
    # 创建客户端实例
    OrderClient2 = L2TCPClient(server, 18103)
    
    # 连接到服务器
    OrderClient2.connect()
    print(OrderClient2.subStock("000001.SZ"))
    print(OrderClient2.subStock("000002.SZ"))
    # 在新线程中处理接收数据  注意不要使用loginStock
    thread2 = threading.Thread(target=Receive_data_thread, args=(OrderClient,"Order"))
    thread2.start()
    

     # 创建客户端实例
    TranClient = L2TCPClient(server, 18105)
    
    # 连接到服务器
    TranClient.connect()

    print(TranClient.loginStock())
    print(TranClient.subStock("000001.SZ"))
    print(TranClient.subStock("000002.SZ"))
    # 在新线程中处理接收数据
    thread3 = threading.Thread(target=Receive_data_thread, args=(TranClient,"Tran"))
    thread3.start()

    

   