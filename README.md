Este é um projeto de chat que utiliza comunicação **TCP/IP** entre um servidor e vários clientes. A interface gráfica é implementada usando **Tkinter**, e a integridade das mensagens é garantida pelo uso de hashes **MD5**.

## Como executar corretamente
- Primeiro executar o servidor.py
- Depois execute uma vez o cliente.py
- Para abrir outros clientes, execute o comando `python cliente.py` diretamente pelo terminal ou CMD.
  ```bash
      python cliente.py
  ``` 
---

## Resumo de como funciona o programa

### Servidor

O servidor cria uma interface gráfica que permite monitorar conexões e mensagens recebidas de clientes. Ele escuta na porta **12345** e utiliza o protocolo **TCP**. Quando um cliente envia uma mensagem, o servidor verifica sua integridade usando **MD5**, armazena a mensagem em um log e distribui para os demais clientes conectados, funcionando como um chat em rede.

#### 1. Interface Gráfica:
- A interface gráfica, criada com **Tkinter**, exibe mensagens e eventos (como conexões) em uma área de texto **ScrolledText**.

#### 2. Iniciar Servidor:
- O servidor inicia criando um socket **TCP** que escuta na porta **12345** do **localhost**.
- A função de escuta roda em uma **thread separada**, mantendo a interface gráfica responsiva.

#### 3. Aceitar Conexões:
- O servidor aceita conexões de clientes e cria um socket dedicado para cada um.
- Cada cliente recebe um **ID único**, e essa informação é exibida na interface gráfica do servidor.

#### 4. Receber e Verificar Mensagens:
- As mensagens enviadas pelos clientes incluem um hash **MD5** da mensagem.
- O servidor verifica a integridade da mensagem recalculando o hash e comparando com o hash recebido.

#### 5. Registro de Mensagens:
- Mensagens válidas são registradas em um arquivo de log (`mensagens_log.txt`), juntamente com os detalhes dos hashes, do ID do cliente e horário.

#### 6. Distribuir Mensagens:
- O servidor distribui as mensagens recebidas para todos os outros clientes conectados, exceto para o cliente que enviou a mensagem originalmente.

#### 7. Tratamento de Erros:
- O servidor lida com erros de comunicação, removendo clientes desconectados sem interromper sua operação.

---

### Cliente

O cliente cria uma interface gráfica que permite enviar mensagens para o servidor e receber mensagens de outros clientes conectados. As mensagens são enviadas com um hash **MD5** para garantir integridade, e as respostas do servidor são exibidas em tempo real.

#### 1. Interface Gráfica:
- A GUI, feita com **Tkinter**, contém um campo para o usuário digitar mensagens, um botão de envio, e uma área de texto **ScrolledText** para exibir mensagens recebidas.

#### 2. Iniciar Cliente:
- O cliente se conecta ao servidor na **localhost** (127.0.0.1) na porta **12345**.
- Um **ID único** é atribuído ao cliente pelo servidor e exibido na interface gráfica.

#### 3. Enviar Mensagem:
- Quando o usuário envia uma mensagem, o cliente calcula o hash **MD5** e envia tanto a mensagem quanto o hash ao servidor.

#### 4. Receber Respostas:
- O cliente usa uma **thread separada** para monitorar mensagens recebidas do servidor em tempo real.

#### 5. Exibir Mensagens:
- As mensagens recebidas do servidor são exibidas na área de texto da GUI do cliente.

#### 6. Registro em log:
- As mensagens são registradas no arquivo de log (`mensagens_log.txt`).

---

## Outros detalhes do programa

#### 1. Uso de Hashes:
- **Integridade da Mensagem**: As mensagens enviadas pelos clientes incluem um hash **MD5**. O servidor recalcula o hash para garantir que a mensagem não foi alterada durante o envio.

#### 2. Uso de Threads:
- **Execução Paralela**: O servidor e o cliente utilizam **threads** para executar operações de rede e manter a interface gráfica responsiva. Isso permite que o cliente e o servidor recebam e enviem mensagens sem bloquear a interface.

## Referencias parciais
- **Tkinter:** https://docs.python.org/pt-br/3/library/tkinter.html
- **Threading:** https://docs.python.org/pt-br/3/library/threading.html
- **Hashlib:** https://pt.stackoverflow.com/questions/398124/como-criar-um-hash-usando-a-biblioteca-hashlib-usando-o-metodo-time-time-em
- **Hashlib:** https://docs.python.org/pt-br/3/library/hashlib.html
