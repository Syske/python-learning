# 导入模块
import os
import socket
import http.server
import socketserver
import cgi

# 定义要分享的文件夹路径
folder_path = "./"

# 获取本地电脑的IP地址
ip_address = socket.gethostbyname(socket.gethostname())

# 定义端口号，可以自己修改
port = 8000

# 切换到文件夹路径
os.chdir(folder_path)

# 创建一个HTTP请求处理器类，用于显示文件夹内容和上传文件
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # 调用父类的方法，获取文件夹内容列表
        files = super().list_directory(path)
        # 在列表开头添加一个返回上级目录的链接和一个上传文件的表单
        files.insert(0, b'<a href="../">../</a>\n')
        files.insert(1, b'<form enctype="multipart/form-data" method="post"><input name="file" type="file"/><input type="submit" value="Upload"/></form>\n')
        return files
    
    def do_POST(self):
        # 处理POST请求，用于接收上传的文件并保存到当前目录下
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                         'CONTENT_TYPE':self.headers['Content-Type']})
        # 获取上传的文件对象和名称
        file_item = form["file"]
        file_name = file_item.filename
        
        # 打开一个新文件，并将上传的文件内容写入其中，然后关闭文件
        with open(file_name, "wb") as f:
            f.write(file_item.file.read())
        
        # 发送响应头和状态码给客户端，并结束响应头部分
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # 发送响应内容给客户端，显示上传成功的信息，并提供返回链接
        self.wfile.write(b"<html><head><title>Upload Success</title></head>")
        self.wfile.write(b"<body><h1>Upload Success</h1>")
        self.wfile.write(b"<p>You have uploaded: %s</p>" % file_name.encode())
        self.wfile.write(b"<p><a href='./'>Go back</a></p>")
        
# 创建一个HTTP服务器对象，绑定IP地址和端口号，并设置请求处理器类为MyHandler
httpd = socketserver.TCPServer((ip_address, port), MyHandler)

# 打印提示信息，告诉用户如何访问分享的文件夹或者上传文件到该文件夹下。
print(f"Sharing folder {folder_path} on http://{ip_address}:{port}")
print(f"You can also upload files to this folder from your phone or other devices.")

# 启动服务器，等待连接请求。
httpd.serve_forever()