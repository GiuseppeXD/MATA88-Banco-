import socket
import struct
import time
from _thread import *
from threading import Thread 
from socketserver import ThreadingMixIn 
from Banco import Banco


# ----- START INITIAL SETTINGS -----

HOST = '0.0.0.0'
PORT = 5002
BUFFER_SIZE = 2048
threads = 0
STATE = ''
SAVED_STATE = False
LIST_CLIENTS = []

# ----------

class Reset_State(Thread):
    def __init__(self):
        Thread.__init__(self)
        time.sleep(15000)
        SAVED_STATE = False


class SnapShot(Thread):
    def __init__(self, socketServer):
        Thread.__init__(self)
        self.socketServer = socketServer

    def sendMark(self):
        for conn in LIST_CLIENTS:
            conn.send(bytes("save", "utf-8"))
        print("Estado do Servidor :" + STATE)
        SAVED_STATE = True
        reset = Reset_State()
        reset.start()





class ClientThread(Thread): # ----- THREAD FOR A NEW CLIENT -----
    def __init__(self, id, ip, port, connection, snapshot):
        Thread.__init__(self)

        # SET IP, PORT AND HANDLE CONNECTION TO CLIENT THREAD
        self.snapshot = snapshot
        self.id = id
        self.ip = ip
        self.port = port
        self.connection = connection
        print("Thread Cliente "+str(id)+" criada")

    
    def run(self): # ----- EXECUTION OF EACH CLIENT THREAD -----

        while True:
            # ----- LOOP TO GET DATA TO AUTHENTICATION SENDED OF CLIENT -----
            data = ''
            while True:

                data = self.connection.recv(BUFFER_SIZE).decode("utf-8").split(' ') # GET DATA SENDED BY CLIENT

                if data[0] == '1': # LOGIN OPTION
                    res = Banco.login(data[1], data[2]) # QUERY BY A USER IN DATABASE

                    self.connection.send(bytes([res])) # SEND RESPONSE OF DATABASE TO CLIENT
                    if res == 0: break # IF FIND A USER, LEAVE LOOP

                elif data[0] == '2': # REGISTER OPTION
                    res = Banco.register(data[1], data[2], data[3]) # REGISTER A USER IN DATABASE

                    self.connection.send(bytes([res])) # SEND RESPONSE OF DATABASE TO CLIENT

                else: # ANOTHER OPTION
                    print("Thread Cliente "+str(self.id)+" fechada")
                    self.connection.close()
                    return
                

            # ----- LOOP TO HANDLE OPERATIONS OF CLIENT -----
            data = ''
            self.messages = []
            while True:
                STATE = data

                data = self.connection.recv(BUFFER_SIZE).decode("utf-8").split(' ') # GET OPERATION SENDED BY CLIENT
                self.messages.append(data)
                if data[0] == '0': # OPERATION QUERY CASH
                    res = Banco.queryCash(data[1]) # QUERY CASH MONEY
                    self.connection.send(bytes(" ".join(["QUERY" , str(res)]), "utf-8")) # SEND RESPONSE OF DATABASE TO CLIENT

                elif data[0] == '1': # OPERATION WITHDRAW
                    res = Banco.withdraw(data[1], int(data[2])) # WITHDRAWING MONEY
                    self.connection.send(bytes(" ".join(["WITHDRAWING" , str(res)]), "utf-8")) # SEND RESPONSE OF DATABASE TO CLIENT

                elif data[0] == '2': # OPERATION DEPOSIT
                    res = Banco.deposit(data[1], int(data[2])) # DEPOSITING MONEY
                    self.connection.send(bytes(" ".join(["DEPOSITING" , str(res)]), "utf-8")) # SEND RESPONSE OF DATABASE TO CLIENT

                elif data[0] == '3': # OPERATION TRANSFER
                    res = Banco.transfer(data[1], int(data[2]), data[3]) # TRANSFERING MONEY TO ANOTHER CLIENT
                    self.connection.send(bytes(" ".join(["TRANSFER" , str(res)]), "utf-8")) # SEND RESPONSE OF DATABASE TO CLIENT

                elif data[0] == '4': # OPERATION LOGOUT
                    self.connection.send(bytes("LOGOUT", "utf-8"))
                    break

                elif data[0] == 'save':
                    if SAVED_STATE:
                        print(self.messages)
                        self.messages = []
                    else:
                        self.snapshot.sendMark()

                else: # ANOTHER OPERATION CLOSES THE CONNECTION
                    print("Thread Cliente "+str(self.id)+" fechada")
                    self.connection.close()
                    return


# ----- INITIALIZES SOCKET CONFIGURATION -----

socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServer.bind((HOST, PORT))
socketServer.listen(1)

snapshot = SnapShot(socketServer)
snapshot.start()

# ----------

while True:    
    (conn, (host, port)) = socketServer.accept() # WAITING A CONNECTION OF CLIENT
    LIST_CLIENTS.append(conn)
    threads += 1 # INCREMENTS NUMBER OF THREAD
    newThread = ClientThread(threads, host, port, conn, snapshot) # CREATES THREAD TO NEW CLIENT
    newThread.start() # RUN THREAD

