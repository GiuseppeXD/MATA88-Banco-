import socket
from threading import Thread
from Banco import Banco

TCP_IP = '0.0.0.0'
TCP_PORT = 5000
BUFFER_SIZE = 20
banco = Banco()

class ClientThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print("Thread Cliente Criada")

    def run(self):
        while True:
            data = self.conn.recv(2048).decode("utf-8")
            print(data)
            campos = data.split(' ')
            if campos[0] == "criar":
                retorno = banco.CriarCliente(campos[1], campos[2], campos[3]) #Criar RG Senha Nome
                if retorno:
                    conn.send(bytes("Sucesso", 'utf-8'))
                    break
                else:
                    conn.send(bytes("Usuario Ja Existente", 'utf-8'))
            retorno = banco.ConsultarClient(campos[0], campos[1])
            if  retorno == 1:
                conn.send(bytes("Sucesso", 'utf-8'))
                break
            elif retorno == 2:
                conn.send(bytes("Senha Incorreta", 'utf-8'))
            else:
                conn.send(bytes("Usuario Inexistente", 'utf-8'))

        while True:
            data = self.conn.recv(2048).decode("utf-8")
            print(data)
            if data == "exit":
                conn.send(bytes("Bye !", 'utf-8'))
            conn.send(bytes("Fodase por enquanto", 'utf-8'))


tcpServer =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port, conn)
    threads.append(newthread)
    newthread.start()

for t in threads:
    t.join()

