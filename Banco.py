

class Banco:
    def __init__(self):
        f = open("banco.txt", 'a')
        f.close()

    def ConsultarClient(self, rgcliente, senha):
        f = open("banco.txt", 'r')
        with f:
            line = f.readline()
            while line:
                campos = line.split(' ')
                if campos[0] == rgcliente:
                    print("Cliente Encontrado")
                    if campos[1] == senha:
                        print("Acesso permitido")
                        return 1
                    else:
                        print("Senha Incorreta")
                        return 2
                line = f.readline()
            print("Cliente Nao Encontrado")
            return 3





    def ConsultarSaldo(self, rgcliente, printar=False):
        f = open("banco.txt", 'r')
        with f:
            line = f.readline()
            while line:
                campos = line.split(' ')
                if campos[0] == rgcliente:
                    if printar:
                        print("Cliente : ", campos[2], " Saldo Atual : ", campos[3])
                    return campos[3]
                line = f.readline()
            print("Cliente Nao Encontrado")
            return False

    def mudarSaldo(self, rgcliente, valor):
        f = open("banco.txt", 'r+')
        with f:
            line = f.readline()
            anterior = 0
            proximo = f.tell()
            while line:
                campos = line.split(' ')
                if campos[0] == rgcliente:
                    campos[3] = valor
                    return campos[3]
                line = f.readline()
                anterior = proximo
                proximo = f.tell()
            print("Cliente Nao Encontrado")
            return False

    def salvarArquivo(self):
        f = open("banco.txt", 'w')
        with f:
            for cliente in self.clientesSenhas:
                f.write(str(cliente) + ' ' + str(self.clientesSenhas[cliente]) + ' '
                        + str(self.clientesSaldos[cliente]) + '\n')


