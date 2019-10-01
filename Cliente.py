import socket

host = socket.gethostname()
port = 5000
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

data = ''

while data!="Sucesso":
    usu = input("Usuario : ")
    senha = input("Senha : ")
    tcpClientA.send(bytes(usu + ' ' + senha, 'utf-8'))
    data = tcpClientA.recv(BUFFER_SIZE).decode("utf-8")
    print(data)

MESSAGE = ''

while MESSAGE!="exit":
    MESSAGE = input("Operacao : ")
    tcpClientA.send(bytes(MESSAGE, 'utf-8'))
    data = tcpClientA.recv(BUFFER_SIZE).decode("utf-8")
    print(data)

tcpClientA.close()




