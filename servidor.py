'''Christian Matheus Oliveira Chaves
Lucas Coutinho Nascimento
Vinícius Siqueira Cardoso '''

# Importação dos módulos necessários
import socket # Módulo principal de comunicação de rede
import hashlib # Funções de hash
import tkinter as tk # Módulo para gerar interface gráfica
from tkinter import scrolledtext
import threading # Módulo para gerenciamento de threads
from datetime import datetime

class Servidor:
    def __init__(self, root):
        # Funcionalidade adicional (interface para enviar e receber mensagens)
        # Inicializa a interface do servidor e configura o layout
        self.root = root
        self.root.title("Socket - Servidor")

        # Área de texto para exibir as mensagens no servidor
        self.mensagem_text = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
        self.mensagem_text.pack(pady=5)

        # Lista para armazenar os clientes conectados
        self.clientes = []
        # Contador para identificar cada cliente que se conecta
        self.cliente_id = 0
        
        # Contador para registrar a quantidade de mensagens no arquivo de log
        self.contador_mensagens = 0
        
        # Variável para registrar o horário da mensagem
        self.hora_atual = datetime.now().strftime("%H:%M:%S")
        
        self.iniciar_servidor()

    def iniciar_servidor(self):
        # Cria o socket do servidor e coloca-o em modo de escuta
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind(('localhost', 12345))  # Associa ao endereço localhost e porta
        self.servidor_socket.listen(5)  # Limita o servidor a 5 conexões simultâneas
        self.adicionar_mensagem("Servidor aguardando conexões...")

        # Inicia uma thread separada para aceitar conexões dos clientes
        threading.Thread(target=self.aceitar_conexoes).start()

    def aceitar_conexoes(self):
        # Aceita conexões de clientes de forma contínua
        while True:
            con, ende = self.servidor_socket.accept()
            self.cliente_id += 1  # Incrementa o ID do cliente a cada nova conexão
            self.clientes.append((con, self.cliente_id))  # Armazena o socket e o ID do cliente
            self.adicionar_mensagem(f"Conectado ao Cliente {self.cliente_id}: {ende}")

            # Envia o ID do cliente para ser exibido na interface do cliente
            con.send(str(self.cliente_id).encode())

            # Inicia uma nova thread para gerenciar a comunicação com o cliente
            threading.Thread(target=self.gerenciar_cliente, args=(con, self.cliente_id)).start()

    def gerenciar_cliente(self, con, cliente_id):
        # Gerencia a comunicação com um cliente específico
        while True:
            try:
                # Recebe a mensagem e o hash do cliente
                data = con.recv(1024)
                if not data:
                    break

                # Decodifica a mensagem recebida
                mensagem_completa = data.decode()
                if '|' in mensagem_completa:
                    # Separa a mensagem do hash recebido
                    mensagem, hash_recebido = mensagem_completa.split('|', 1)
                    # Calcula o hash MD5 da mensagem recebida
                    hash_calculado = hashlib.md5(mensagem.encode()).hexdigest()

                    # Verifica a integridade da mensagem comparando os hashes
                    verificado = "Bem-sucedida" if hash_recebido == hash_calculado else "Falha"
                    
                    # Incrementa o contador de mensagens
                    self.contador_mensagens += 1

                    # Registra a mensagem no log
                    self.registrar_mensagem(mensagem, hash_recebido, hash_calculado, verificado, cliente_id)

                    # Envia a mensagem recebida para os outros clientes
                    self.distribuir_mensagem(mensagem, cliente_id)

            except:
                break

    def distribuir_mensagem(self, mensagem, cliente_id):
        # Funcionalidade adicional (envio de mensagens entre multiplos clientes)
        # Envia a mensagem para o outro cliente conectado
        for cliente, id_cliente in self.clientes:
            if id_cliente != cliente_id:
                try:
                    cliente.send(mensagem.encode())  # Envia apenas a mensagem
                except:
                    # Remove o cliente se houver erro na comunicação
                    self.clientes.remove((cliente, id_cliente))

    def registrar_mensagem(self, mensagem, hash_recebido, hash_calculado, verificado, cliente_id):
        # Funcionalidade adicional (registro de mensagens e hash em um arquivo de log)
        # Registra a mensagem no arquivo de log com detalhes da hash
        with open('mensagens_log.txt', 'a', encoding='UTF8') as file:
            file.write(f" {self.contador_mensagens}. [{self.hora_atual}] Cliente {cliente_id}\n")
            file.write(f"Mensagem: {mensagem}\n")
            file.write(f"Hash Recebido: {hash_recebido}\n")
            file.write(f"Hash Calculado: {hash_calculado}\n")
            file.write(f"Verificação: {verificado}\n")
            file.write("-------------------------\n")

    def adicionar_mensagem(self, mensagem):
        # Exibe a mensagem na área de texto do servidor
        self.mensagem_text.config(state='normal')
        self.mensagem_text.insert(tk.END, mensagem + '\n')
        self.mensagem_text.config(state='disabled')
        self.mensagem_text.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = Servidor(root)
    root.mainloop()
