

class Banco:
    @staticmethod
    def openFile():
        f = open("banco.txt", 'a')
        f.close()

        return open("banco.txt", 'r+')
    
    @staticmethod
    def ConsultarClient(rgClient, pwdClient):
        file = Banco.openFile()

        with file:
            line = file.readline()

            while line:
                [username, rg, password, cash] = line.split('|')

                if rg == rgClient:
                    print("Cliente encontrado")
                    if password == pwdClient:
                        print("Acesso permitido")
                        return 0
                    else:
                        print("Senha incorreta")
                        return 1

                line = file.readline()

            print("Cliente não encontrado")
            return 2




    @staticmethod
    def getCash(file, rg):
        for line in file:
            if rg in line:
                return int(line.split('|')[3])

    @staticmethod
    def withdraw(rg, value):
        file = Banco.openFile()
        cash = Banco.getCash(file, rg)

        if cash < value:
            print('Saldo insuficiente')
            return 1
        
        cash -= value

        lines = []
        file.seek(0,0)
        for line in file:
            if not rg in line:
                lines.append(line)
            else:
                [user, rg, pwd, oldCash] = line.split('|')
                lines.append("|".join([user, rg, pwd, str(cash)+"\n"]))

        file.seek(0, 0)
        file.truncate()
        file.writelines(lines)
        file.close()

        return 0
    
    @staticmethod
    def deposit(rg, value):
        file = Banco.openFile()
        cash = Banco.getCash(file, rg)
        cash += value

        lines = []
        file.seek(0, 0)
        for line in file:
            if not rg in line:
                lines.append(line)
            else:
                [user, rg, pwd, oldCash] = line.split('|')
                lines.append("|".join([user, rg, pwd, str(cash)+"\n"]))

        file.seek(0, 0)
        file.truncate()
        file.writelines(lines)
        file.close()

        return 0

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


