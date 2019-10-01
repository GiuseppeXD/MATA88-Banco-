import socket
from threading import Thread
from Banco import Banco

# ----- START INITIAL SETTINGS -----

HOST = '0.0.0.0'
PORT = 5001
BUFFER_SIZE = 2048

# ----------

class ClientThread(Thread): # ----- THREAD FOR A NEW CLIENT -----
    def __init__(self, ip, port, connection):
        Thread.__init__(self)

        # SET IP, PORT AND HANDLE CONNECTION TO CLIENT THREAD
        self.ip = ip
        self.port = port
        self.connection = connection
        print("Thread Cliente Criada")

    
    def run(self): # ----- EXECUTION OF EACH CLIENT THREAD -----

        # ----- GET DATA TO AUTHENTICATION SENDED OF CLIENT -----

        while True:
            [rg, password] = self.connection.recv(BUFFER_SIZE).decode("utf-8").split(' ') # GET LOGIN SENDED BY CLIENT
            res = Banco.ConsultarClient(rg, password) # QUERY BY A USER IN DATABASE

            self.connection.send(bytes([res])) # SEND RESPONSE OF DATABASE TO CLIENT
            if res == 0: break # IF FIND A USER, LEAVE LOOP
            

        # ----- LOOP TO HANDLE OPERATIONS OF CLIENT -----

        while True:
            data = self.connection.recv(BUFFER_SIZE).decode("utf-8").split(' ') # GET OPERATION SENDED BY CLIENT

            if data[0] == '1':
                res = Banco.withdraw(data[1], int(data[2]))
                self.connection.send(bytes([res]))

            if data[0] == '2':
                res = Banco.deposit(data[1], int(data[2]))
                self.connection.send(bytes([res]))

            if data[0] == '4':
                conn.send(bytes("Bye !", 'utf-8'))
                conn.send(bytes("Fodase por enquanto", 'utf-8'))


socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServer.bind((HOST, PORT))
threads = []

while True:
    socketServer.listen(1)

    (conn, (host, port)) = socketServer.accept()
    newthread = ClientThread(host, port, conn)
    newthread.start()

    threads.append(newthread)

for t in threads:
    t.join()

