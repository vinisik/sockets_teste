## Resumo de como funciona o programa
## Servidor
O servidor cria uma interface gráfica para monitoramento e escuta conexões de clientes em uma porta específica. Quando um dos clientes envia uma mensagem, o servidor verifica a integridade da mensagem usando um hash MD5, registra a mensagem em um arquivo, atualiza um contador de mensagens, e exibe a mensagem na interface do outro cliente, funcionando como uma espécie de chat utilizando protocolo TCP. Todo o processo de comunicação e registro é executado em paralelo com a interface gráfica, garantindo que o servidor continue responsivo.

#### 1. Interface Gráfica
- Utiliza o módulo **tkinter** para criar uma interface gráfica que exibe as mensagens recebidas dos clientes e outros eventos, como conexões e erros. A interface inclui uma área de texto **(ScrolledText)** onde essas informações são exibidas.

#### 2. Iniciar Servidor
- O servidor é iniciado ao criar um socket **TCP** que escuta por conexões na **localhost** na porta **12345**.
- O servidor entra em modo de escuta (listen) e aguarda conexões de clientes. Este processo é executado em uma thread separada para que a interface gráfica continue responsiva.

#### 3. Aceitar Conexões
- A função aceitar_conexoes é executada em uma thread separada. Ela aceita conexões de clientes e cria um novo socket para se comunicar com cada cliente.
- Quando um cliente se conecta, o servidor exibe o endereço do cliente na interface gráfica.

#### 4. Receber e Verificar Mensagens:
- O servidor recebe dados (mensagens) dos clientes em pacotes de até 1024 bytes.
- A mensagem recebida é dividida em duas partes: o texto da mensagem e o hash MD5 que o cliente enviou junto.
- O servidor recalcula o hash MD5 da mensagem recebida e o compara com o hash enviado pelo cliente para verificar se a mensagem chegou sem alterações.

#### 5. Registro de Mensagens:
- Se a verificação de integridade for bem-sucedida, o servidor registra a mensagem em um arquivo de texto (mensagens_recebidas.txt), incluindo detalhes como a mensagem, os hashes recebidos e calculados, e o resultado da verificação.
- O servidor também mantém um contador de mensagens, que é atualizado e salvo em um arquivo separado (contador.txt).

#### 6. Resposta ao Cliente:
- Após verificar a integridade da mensagem e registrá-la, o servidor envia uma resposta ao cliente, indicando se a mensagem foi recebida com sucesso ou se houve falha na verificação de integridade.

#### 7. Manipulação de Erros:
- Caso ocorra algum erro durante a comunicação com o cliente, o servidor captura a exceção, exibe uma mensagem na interface gráfica, e continua a operação.


## Cliente
O programa cria uma interface gráfica que permite enviar mensagens para um servidor TCP. Ele usa threading para manter a interface responsiva enquanto o cliente se comunica com o servidor. As mensagens são enviadas junto com um hash MD5 para garantir sua integridade. As respostas do servidor são exibidas na interface gráfica em tempo real.

#### 1. Interface Gráfica:
- A interface gráfica é criada utilizando o módulo tkinter. Ela inclui um campo para digitar a mensagem, um botão para enviar a mensagem, e uma área de texto para exibir as respostas recebidas do servidor.

#### 2. Iniciar Cliente:
- Ao iniciar o programa, um socket TCP é criado em uma thread separada. Essa thread executa a função iniciar_cliente, que conecta o cliente a um servidor rodando no localhost na porta 12345.
- A thread permite que a interface gráfica permaneça responsiva enquanto o cliente aguarda mensagens do servidor.

#### 3. Enviar Mensagem:
- Quando o usuário digita uma mensagem e clica no botão "Enviar", a função enviar_mensagem é chamada.
- A mensagem é concatenada com um hash MD5 gerado a partir da própria mensagem. O hash garante a integridade da mensagem, permitindo que o servidor verifique se ela não foi alterada durante o envio.
- A mensagem e o hash são enviados ao servidor via socket.

#### 4. Receber Resposta:
- A função iniciar_cliente, em execução na thread separada, fica continuamente esperando por respostas do servidor.
- Quando uma resposta é recebida, ela é exibida na área de texto da interface gráfica.

#### 5. Exibição de Respostas:
- As respostas do servidor são exibidas na área de texto (ScrolledText), e a interface é atualizada automaticamente para mostrar as novas mensagens recebidas.




## Outros detalhes do programa
##### 1. Uso de Hashes

- **Integridade da Mensagem:** A função de hash hashlib.md5 é utilizada para calcular o hash MD5 da mensagem que o usuário deseja enviar ao servidor. Isso garante a integridade da mensagem, permitindo que o servidor verifique se a mensagem não foi alterada durante o trânsito. Ao enviar a mensagem junto com seu hash, o servidor pode recalcular o hash da mensagem recebida e compará-lo com o hash enviado, detectando possíveis modificações.

#### 2. Uso do Threading
- **Execução Paralela:** O módulo threading é utilizado para executar a função iniciar_cliente em uma thread separada. Essa função é responsável por manter a conexão com o servidor e receber mensagens continuamente. Ao rodar essa função em uma thread separada, a interface gráfica do Tkinter (root.mainloop()) permanece responsiva, permitindo ao usuário interagir com a GUI enquanto as mensagens do servidor são recebidas em segundo plano. Sem o uso de threading, a interface gráfica poderia ficar bloqueada ou travar enquanto espera por mensagens do servidor.


## Referencias parciais
- **Tkinter:** https://docs.python.org/pt-br/3/library/tkinter.html
- **Threading:** https://docs.python.org/pt-br/3/library/threading.html
- **Hashlib:** https://pt.stackoverflow.com/questions/398124/como-criar-um-hash-usando-a-biblioteca-hashlib-usando-o-metodo-time-time-em
- **Hashlib:** https://docs.python.org/pt-br/3/library/hashlib.html
