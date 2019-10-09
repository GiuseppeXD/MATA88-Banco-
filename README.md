# MATA88-Banco-
Trabalho de Sistemas Distribuídos Simulação Banco-Servidor com Threads para atender Clientes

Inicialização:
  Em um computadores diferentes deve-se recuperar o ip da máquina que executará Servidor.py e coloca-lo no campo HOST do Cliente.py
  Num mesmo computador deve-se abrir um terminal e executar o Servidor.py, após isso cada novo terminal executando Cliente.py será um cliente
  
Opções no Cliente:
  O cliente inicialmente tem 3 opções:
    *Realizar Login informando RG e Senha de um Usuário já Cadatrado no Banco.
    *Realizar Cadastro de um Usuário no Banco informando RG, Nome do Usuário, e Senha (obs: todas as contas iniciam com saldo zerado).
    *Finalizar execução do Cliente.py
    
  Assim que devidamente Logado no Banco, o cliente terá 5 opções:
    *Realizar consulta de Saldo
    *Realizar saque de determinado valor a ser informado, operação esta podendo não ser realizada se o saldo for ficar negativo após saque
    *Realizar Depósito de determinado valor a ser informado.
    *Realizar uma Transferencia entre Contas, sendo necessário informar Conta do correntista destino e valor, podendo não ser realizada se o usuário informado não existir, ou se não a saldo suficiente para realizar a transferencia.
    *Finalizar sessão do usuário
  
   
