import socket
import threading
import os
import time
from datetime import datetime

# Рабочая директория сервера
WEB_ROOT = './web_root'

# HTTP-заголовок ответа
SERVER_NAME = "SimplePythonServer/0.1"

def get_http_header(content_length, content_type="text/html"):
    date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    return f"""HTTP/1.1 200 OK
Date: {date}
Content-Type: {content_type}
Server: {SERVER_NAME}
Content-Length: {content_length}
Connection: close

"""

# Создание рабочей директории и файлов
os.makedirs(WEB_ROOT, exist_ok=True)
with open(os.path.join(WEB_ROOT, 'index.html'), 'w') as f:
    f.write('<H1>Index File</H1>')
with open(os.path.join(WEB_ROOT, '1.html'), 'w') as f:
    f.write('<H1>First file</H1>')
with open(os.path.join(WEB_ROOT, '2.html'), 'w') as f:
    f.write('<H1>Second file</H1>')

def handle_client_connection(conn, addr):
    try:
        print("Connected", addr)
        data = conn.recv(8192)
        msg = data.decode()
        print(msg)
        
        # Разбор строки запроса
        request_line = msg.splitlines()[0]
        request_method, path, _ = request_line.split()
        
        if path == '/':
            path = '/index.html'
        
        file_path = os.path.join(WEB_ROOT, path[1:])
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                response_body = f.read()
            content_length = len(response_body)
            response_header = get_http_header(content_length)
        else:
            response_body = '<H1>404 Not Found</H1>'
            content_length = len(response_body)
            response_header = get_http_header(content_length)
        
        response = response_header + response_body
        conn.send(response.encode())
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def start_server():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
    except OSError:
        sock.bind(('', 8080))
    sock.listen(5)
    print("Server started on port 80 or 8080")
    
    while True:
        conn, addr = sock.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
