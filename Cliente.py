import socket

# ----- START INITIAL SETTINGS -----

HOST = socket.gethostname()
PORT = 5002
BUFFER_SIZE = 2048

# ----------

def handleAuth(statusCode): # FUNCTION TO HANDLE STATUS CODE RETURNED BY SERVER
    if statusCode == 0:
        print('\nLogin realizado com sucesso!\n')
        return True
    elif statusCode == 1:
        print('\nSenha incorreta, por favor tente novamente.\n')
        return False
    elif statusCode == 2:
        print('\nUsuário inexistente, por favor tente novamente.\n')
        return False

def showOperations(): # FUNCTION TO SHOW OPERATION TO CLIENT
    print('Operações: ')
    print('1 - Saque')
    print('2 - Depósito')
    print('3 - Transferência')
    print('4 - Logout\n')

# ----- INITIALIZES SOCKET CONFIGURATION -----

try:
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect((HOST, PORT))
except:
    print('Erro ao conectar ao servidor.')

# ----- MAKE LOGIN -----

data = ''

while True:
    rg = input("RG: ")
    password = input("Senha: ")
    socketClient.send(bytes(rg + ' ' + password, 'utf-8')) # SEND DATA TO SERVER

    data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER
    data = int.from_bytes(data, byteorder="big") # TRANSFORM DATA TO INT

    if handleAuth(data):
        break

# ----------

showOperations()

# ----- HANDLES CLIENT OPERATIONS -----

while data != '4':
    data = input("Digite o número de uma operação: ")
    
    if data == '1': # OPERATION WITHDRAW
        value = input("Digite o valor a ser sacado: ")
        socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8')) # SEND DATA TO SERVER

        data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER
        data = int.from_bytes(data, byteorder="big") # TRANSFORM DATA TO INT
        
        if data == 0:
            print('Saque efetuado com sucesso!\n')
        elif data == 1:
            print('Saldo insuficiente\n')
        else:
            print('Erro ao sacar\n')

    elif data == '2': # OPERATION DEPOSIT
        value = input("Digite o valor a ser depositado: ")
        socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8')) # SEND DATA TO SERVER

        data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER
        data = int.from_bytes(data, byteorder="big") # TRANSFORM DATA TO INT
        
        if data == 0:
            print('Depósito efetuado com sucesso!\n')
        else:
            print('Erro ao depositar\n')

    elif data == '3': # OPERATION TRANSFER
        value = input("Digite o valor a ser transferido: ")
        dest = input("Digite o RG do correntista: ")
        socketClient.send(bytes(" ".join([data,rg,value, dest]), 'utf-8')) # SEND DATA TO SERVER

        data = socketClient.recv(BUFFER_SIZE) # RECEIVE DATA FROM SERVER
        data = int.from_bytes(data, byteorder="big") # TRANSFORM DATA TO INT

        if data == 0:
            print('Transferência realizada com sucesso!\n')
        elif data == 1:
            print('Saldo insuficiente\n')
        else:
            print('Correntista não encontrado')

# ----------

socketClient.send(bytes('4', 'utf-8')) # SEND MESSAGE FOR SERVER TO CLOSE CONNECTION
print('\nLogout feito com sucesso!\n')

socketClient.close()







