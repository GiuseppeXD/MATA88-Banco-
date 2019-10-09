# Gestor de Contas Bancárias - MATA88 2019.2
### Integrantes
* Igor de Almeida Nascimento
* Giuseppe Luca Mareschi Outerelo

### Descrição
Trabalho de Sistemas Distribuídos - Simulação de um sistema bancário que utiliza modelo cliente-servidor com multithreading.

### Inicialização:
Em computadores diferentes deve-se recuperar o ip da máquina que executará **Servidor.py** e coloca-lo no campo **HOST** do **Cliente.py**. Num mesmo computador deve-se abrir um terminal e executar o **Servidor.py**, após isso cada novo terminal executando **Cliente.py** será um cliente.
  
### Opções no Cliente
O cliente inicialmente tem 3 opções:
* Realizar login informando __RG__ e **SENHA** de um usuário já cadastrado.
* Realizar cadastro de um usuário informando **RG**, **NOME** do usuário, e **SENHA** (Obs: todas as contas iniciam com saldo zerado).
* Finalizar execução do **Cliente.py**
    
Assim que devidamente logado no sistema, o cliente terá 5 opções:
* Realizar consulta do seu saldo atual.
* Realizar saque de determinado valor a ser informado, operação esta podendo não ser realizada se o saldo for **ficar negativo** após saque
* Realizar depósito de determinado valor a ser informado.
* Realizar uma transferencia entre contas, sendo necessário informar valor e a conta do correntista destino , podendo não ser realizada se o usuário informado **não existir** ou se não há **saldo suficiente** para realizar a transferencia.
* Realizar logout do usuário
