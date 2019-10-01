# ----- CLASS REPRESENTING THE DATABASE ----- 

class Banco:
    @staticmethod
    def openFile(): # METHOD TO OPEN FILE 
        f = open("banco.txt", 'a')
        f.close()

        return open("banco.txt", 'r+')

    @staticmethod
    def checkClient(rgClient): # CHECKS IF A CLIENT EXIST
        file = Banco.openFile()

        with file:
            line = file.readline() # GET A LINE OF FILE
            while line: 
                [username, rg, password, cash] = line.split('|') # GET DATA OF A CLIENT
                if rg == rgClient: # VERIFY IF RG IS EQUAL
                    return 0

                line = file.readline()
        return 1
    
    @staticmethod
    def login(rgClient, pwdClient): # LOGIN A CLIENT
        file = Banco.openFile()

        with file:
            line = file.readline() # GET A LINE OF FILE

            while line:
                [username, rg, password, cash] = line.split('|') # GET DATA OF A CLIENT

                # VERIFY IF CLIENT EXIST IN FILE
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
    def getCash(file, rg): # GET CASH OF A CLIENT
        for line in file:
            if rg in line:
                return int(line.split('|')[3])

    @staticmethod
    def withdraw(rg, value): # WITHDRAW MONEY OF A CLIENT
        file = Banco.openFile()

        cash = Banco.getCash(file, rg) 
        if cash < value: # IF CASH IS LESS THAN VALUE, RETURNS
            print('Saldo insuficiente')
            return 1
        
        cash -= value # ELSE TAKE VALUE OF CASH

        # ----- REWRITE FILE WITH NEW CASH OF CLIENT ----

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
        print('Saque efetuado')

        return 0
    
    @staticmethod
    def deposit(rg, value): # DEPOSIT MONEY OF A CLIENT
        file = Banco.openFile()

        cash = Banco.getCash(file, rg)
        cash += value # INCREMENTS VALUE IN CASH

        # ----- REWRITE FILE WITH NEW CASH OF CLIENT ----

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
        print('Depósito efetuado')

        return 0

    @staticmethod
    def transfer(rg, value, rgDest): # DEPOSIT MONEY FROM A CLIENT TO ANOTHER CLIENT
        if Banco.checkClient(rgDest) == 0: # CHECKS IF RG OF RECIPIENT EXIST
            if Banco.withdraw(rg, value) == 0: # WITHDRAW MONEY
                if Banco.deposit(rgDest, value) == 0: # DEPOSIT MONEY TO RECIPIENT
                    print("Transferência efetuada")
                    return 0
            else:
                print("Saldo insuficiente")
                return 1
        else:
            print("Correntista não encontrado")
            return 2



