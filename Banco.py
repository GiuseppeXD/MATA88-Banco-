

class Banco:
    @staticmethod
    def openFile():
        f = open("banco.txt", 'a')
        f.close()

        return open("banco.txt", 'r+')

    @staticmethod
    def checkClient(rgClient):
        file = Banco.openFile()
        with file:
            line = file.readline()
            while line:
                [username, rg, password, cash] = line.split('|')
                if rg == rgClient:
                    return 0
                line = file.readline()
        return 1
    
    @staticmethod
    def LoginClient(rgClient, pwdClient):
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

    @staticmethod
    def transfer(rg, value, rgDest):
        if Banco.checkClient(rgDest) == 0:
            if Banco.withdraw(rg, value) == 0:
                if Banco.deposit(rgDest, value) == 0:
                    print("Transferencia Realizada")
                    return 0
            else:
                print("Transeferencia Nao Realizada, Saldo Insuficiente")
                return 1
        else:
            print("Correntista Nao encontrado")
            return 2



