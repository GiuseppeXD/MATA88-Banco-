import socket
import struct
import time
import threading
from threading import Thread
# ----- START INITIAL SETTINGS -----

HOST = socket.gethostname()
PORT = 5002
BUFFER_SIZE = 2048

# ----------

class RecvThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.waiting_response = False
        self.saved_state = False
        self.messages = []

    def run(self):
        while True:
            try:
                data = socketClient.recv(BUFFER_SIZE).decode("utf-8").split(' ')

                self.last_message = data

                if data[0] == "save":
                    self.recvMark()
                else:
                    if self.saved_state:
                        self.messages.append(data)
                        print('\nMessagens no Canal: ', self.messages, '\n')
                    if data[0] == 'QUERY':
                        queryResponse(data)
                    if data[0] == 'WITHDRAWING':
                        withdrawingResponse(data)
                    if data[0] == 'DEPOSITING':
                        depositingResponse(data)
                    if data[0] == 'TRANSFER':
                        transferResponse(data)
                    if data[0] == 'LOGOUT':
                        socketClient.setblocking(True)
                        break

                    if self.saved_state == False:
                        self.sendMark()

                    self.waiting_response = False
            except:
                pass
    
    def resetState(self):
        if self.saved_state:
            time.sleep(10)
            self.saved_state = False

    def sendMark(self):
        self.messages = []
        print('Estado do Cliente: ', self.last_message, '\n')
        print('\nMessagens no Canal: ', self.messages, '\n')
        self.saved_state = True
        
        socketClient.send(bytes('save', 'utf-8'))
        reset = threading.Thread(target = self.resetState)
        reset.start()


    def recvMark(self):
        if self.saved_state == False:
            self.sendMark()                

        
def handleRegister(statusCode):
    if statusCode == 0:
        print('\nUsuário cadastrado com sucesso!')
        return True
    elif statusCode == 1:
        print('\nJá existe um usuário com este RG.')
        return False

def handleAuth(statusCode): # FUNCTION TO HANDLE STATUS CODE RETURNED BY SERVER
    if statusCode == 0:
        print('\nLogin realizado com sucesso!')
        return True
    elif statusCode == 1:
        print('\nSenha incorreta.')
        return False
    elif statusCode == 2:
        print('\nUsuário inexistente.')
        return False

def showOptions(): # FUNCTION TO SHOW OPTIONS TO CLIENT
    print('\nOpções: \n1 - Login\n2 - Cadastrar\n3 - Sair\n')

def showOperations(): # FUNCTION TO SHOW OPERATION TO CLIENT
    print('\nOperações: \n0 - Saldo\n1 - Saque\n2 - Depósito\n3 - Transferência\n4 - Logout\n')

def queryResponse(data):
    print('Seu saldo atual é de:', int(data[1]))

def withdrawingResponse(data):

    data = int(data[1]) # TRANSFORM DATA TO INT

    if data == 0:
        print('\nSaque efetuado com sucesso!\n')
    elif data == 1:
        print('\nSaldo insuficiente.\n')
    else:
        print('\nErro ao sacar.\n')

def depositingResponse(data):

    data = int(data[1])  # TRANSFORM DATA TO INT

    if data == 0:
        print('\nDepósito efetuado com sucesso!\n')
    else:
        print('\nErro ao depositar.\n')

def transferResponse(data):
    data = int(data[1])  # TRANSFORM DATA TO INT

    if data == 0:
        print('\nTransferência realizada com sucesso!\n')
    elif data == 1:
        print('\nSaldo insuficiente.\n')
    else:
        print('\nCorrentista não encontrado.\n')

def register():
    while True:
        nome = input("Nome: ")
        rg = input("RG: ")
        password = input("Senha: ")
        socketClient.send(bytes('2 ' + nome + ' ' + rg + ' ' + password, 'utf-8')) # SEND DATA TO SERVER
        
        data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER

        if not data: # HANDLE DATA
            raise

        data = int.from_bytes(data, byteorder="big") # TRANSFORM DATA TO INT

        if handleRegister(data) == False:
            tryAgain = input('Deseja tentar novamente? (y/n) ')
            if tryAgain == 'y':
                continue
            else:
                break
        else: 
            break

def login():
    while True:
        rg = input("RG: ")
        password = input("Senha: ")
        socketClient.send(bytes('1 ' + rg + ' ' + password, 'utf-8'))  # SEND DATA TO SERVER

        data = socketClient.recv(BUFFER_SIZE)  # RECEIVE DATA FROM SERVER

        if not data:  # HANDLE DATA
            raise

        data = int.from_bytes(data, byteorder="big")  # TRANSFORM DATA TO INT

        if handleAuth(data) == False:
            tryAgain = input('Deseja tentar novamente? (y/n) ')
            if tryAgain == 'y':
                continue
            else:
                return
        else:
            break

    socketClient.setblocking(False)
    recv = RecvThread()
    recv.start()

    while True:
        showOperations()
        data = input("Digite o número de uma operação: ")

        if data == '0':
            socketClient.send(bytes(" ".join([data,rg]), 'utf-8')) # SEND DATA TO SERVER
            #data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER

            recv.waiting_response = True
            while recv.waiting_response == True:
                pass
        
        elif data == '1': # OPERATION WITHDRAW
            value = input("Digite o valor a ser sacado: ")
            socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8')) # SEND DATA TO SERVER
            #data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER

            recv.waiting_response = True
            while recv.waiting_response == True:
                pass


        elif data == '2': # OPERATION DEPOSIT
            value = input("Digite o valor a ser depositado: ")
            socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8')) # SEND DATA TO SERVER

            #data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER

            recv.waiting_response = True
            while recv.waiting_response == True:
                pass

        elif data == '3': # OPERATION TRANSFER
            value = input("Digite o valor a ser transferido: ")
            dest = input("Digite o RG do correntista: ")
            socketClient.send(bytes(" ".join([data,rg,value, dest]), 'utf-8')) # SEND DATA TO SERVER

            #data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER
            recv.waiting_response = True
            while recv.waiting_response == True:
                pass

        elif data == '4': 
            socketClient.send(bytes('4', 'utf-8')) # SEND MESSAGE FOR SERVER TO CLOSE CONNECTION
            break
        else:
            print('Operação inválida.')



    print('\nLogout feito com sucesso!')

# ----- INITIALIZES SOCKET CONFIGURATION -----

try:
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect((HOST, PORT))

except:
    print('Erro ao conectar ao servidor.')
    exit(0)

# ----- MAKE LOGIN -----

data = ''
print('Bem vindo ao nosso banco! =D')

try:
    
    while True:
        showOptions()
        data = input("Digite o número de uma opção: ")

        if data == '1':
            login()
        elif data == '2':
            register()
        elif data == '3':
            break
        else:
            print('Opção inválida.')


except:
    print('Algum erro ocorreu ao enviar ou receber dados do servidor.')
    exit(0)


socketClient.send(bytes('3', 'utf-8')) # SEND MESSAGE FOR SERVER TO CLOSE CONNECTION
print('\nAté a próxima!')

socketClient.close()







