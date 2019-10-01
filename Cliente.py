import socket

# ----- START INITIAL SETTINGS -----

HOST = socket.gethostname()
PORT = 5001
BUFFER_SIZE = 2048

# ----------

def handleAuth(statusCode):
    if statusCode == 0:
        print('\nLogin realizado com sucesso!\n')
        return True
    elif statusCode == 1:
        print('\nSenha incorreta, por favor tente novamente.\n')
        return False
    elif statusCode == 2:
        print('\nUsuário inexistente, por favor tente novamente.\n')
        return False

def showOperations():
    print('Operações: ')
    print('0 - Sair')
    print('1 - Saque')
    print('2 - Depósito')
    print('3 - Transferência\n')

try:
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect((HOST, PORT))

except:
    print('Erro ao conectar ao servidor.')

data = ''

while True:
    rg = input("RG: ")
    password = input("Senha: ")

    socketClient.send(bytes(rg + ' ' + password, 'utf-8'))
    data = socketClient.recv(BUFFER_SIZE)
    data = int.from_bytes(data, byteorder="big")
    #print(data)
    if handleAuth(data):
        break

showOperations()

while data != "0":
    data = input("Digite o número de uma operação: ")
    
    if data == '1':
        value = input("Digite o valor a ser sacado: ")
        socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8'))
        data = socketClient.recv(BUFFER_SIZE)
        data = int.from_bytes(data, byteorder="big")
        
        if data == 0:
            print('Saque efetuado com sucesso!')
        elif data == 1:
            print('Saldo insuficiente')
        else:
            print('Erro ao sacar')

    elif data == '2':
        value = input("Digite o valor a ser depositado: ")
        socketClient.send(bytes(" ".join([data,rg,value]), 'utf-8'))
        data = socketClient.recv(BUFFER_SIZE)
        data = int.from_bytes(data, byteorder="big")
        
        if data == 0:
            print('Depósito efetuado com sucesso!')
        else:
            print('Erro ao depositar')

    elif data == '3':
        value = input("Digite o valor a ser transferido: ")
        dest = input("Digite o RG do correntista: ")
        socketClient.send(bytes(" ".join([data,rg,value, dest]), 'utf-8'))
        data = socketClient.recv(BUFFER_SIZE)
        data = int.from_bytes(data, byteorder="big")

        if data == 0:
            print('Transferencia Realizada com sucesso!')
        elif data == 1:
            print('Saldo Insuficiente')
        else:
            print('Correntista nao encontrado')
    
    
   

socketClient.close()







