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

class Cliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket - Cliente")

        # Configuração do layout
        # Funcionalidade adicional
        self.mensagem_label = tk.Label(root, text="Digite a mensagem:")
        self.mensagem_label.pack(pady=5)

        self.mensagem_entry = tk.Entry(root, width=50)
        self.mensagem_entry.pack(pady=5)

        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_mensagem)
        self.enviar_button.pack(pady=5)

        self.resposta_text = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')
        self.resposta_text.pack(pady=5)

        # Inicializa o socket em uma thread separada
        self.cliente_socket = None
        self.thread = threading.Thread(target=self.iniciar_cliente)
        self.thread.start()

    def iniciar_cliente(self):
        # Cria um socket para o cliente usando IPv4 e protocolo TCP
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta o socket ao servidor localhost na porta 12345
        self.cliente_socket.connect(('localhost', 12345))

        while True:
            try:
                # Recebe a resposta do servidor (máximo de 1024 bytes) e converte para string
                response = self.cliente_socket.recv(1024).decode()
                if response:
                    self.exibir_resposta(f"Resposta do servidor: {response}")
            except (socket.error, ConnectionAbortedError):
                break

    def enviar_mensagem(self):
        # Funcionalidade adicional (exibir horario)
        hora = datetime.now()
        hora_atual = hora.strftime("%H:%M:%S")
        
        mensagem = self.mensagem_entry.get()
        if mensagem:
            # Calcula o hash MD5 da mensagem para garantir integridade
            mensagem_hash = hashlib.md5(mensagem.encode()).hexdigest()
            # Envia a mensagem e o hash MD5 ao servidor
            self.cliente_socket.send(f"{mensagem}|{mensagem_hash}".encode())
            self.exibir_resposta(f"Mensagem enviada: {mensagem}"
                                 f"\nHora da mensagem: {hora_atual}")

    # Envia a resposta para a janela do tkinter
    # Funcionalidade adicional (exibir janela)
    def exibir_resposta(self, texto):
        self.resposta_text.config(state='normal')
        self.resposta_text.insert(tk.END, texto + '\n')
        self.resposta_text.config(state='disabled')
        self.resposta_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Cliente(root)
    root.mainloop()