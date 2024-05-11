import socket
import threading
import time
 
 
# 向所有客户端发送数据
def send_msg():
    while True:
        try:
            time.sleep(2)
            server.sendto("Turn on".encode(), host_esp8266)
            time.sleep(2)
        except Exception as e:
            try:
                print("Send Error!")
            except Exception as e:
                pass
 
 
# 接收客户端的数据
def recv_data():
    while True:
        data, addr = server.recvfrom(package_len)
        print(data)
        print(addr)
 
 
package_len = 1420  # 一帧数据长度
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ('192.168.0.104', 8081)
host_esp8266 = ('192.168.0.103', 1234)
server.bind(host)
t0 = threading.Thread(target=recv_data)
t0.start()
t1 = threading.Thread(target=send_msg)
t1.start()