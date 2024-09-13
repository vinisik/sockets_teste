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
        # Inicializa a interface do cliente e configura o layout
        self.root = root
        self.cliente_id = None  # ID do cliente recebido do servidor
        self.root.title(f"Socket - Cliente")

        # Funcionalidade adicional (interface para enviar e receber mensagens)
        # Campo para digitar a mensagem
        self.mensagem_label = tk.Label(root, text="Digite a mensagem:")
        self.mensagem_label.pack(pady=5)

        self.mensagem_entry = tk.Entry(root, width=50)
        self.mensagem_entry.pack(pady=5)

        # Botão para enviar a mensagem
        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_mensagem)
        self.enviar_button.pack(pady=5)

        # Área de texto para exibir as mensagens
        self.resposta_text = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')
        self.resposta_text.pack(pady=5)

        # Socket para comunicação com o servidor
        self.cliente_socket = None
        threading.Thread(target=self.iniciar_cliente).start()
        
        # Variável para registrar o horário da mensagem
        self.hora = datetime.now().strftime("%H:%M")

    def iniciar_cliente(self):
        # Inicializa o socket e conecta ao servidor
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect(('localhost', 12345))

        # Recebe o ID do cliente enviado pelo servidor
        self.cliente_id = self.cliente_socket.recv(1024).decode()
        # Atualiza o título da janela com o ID do cliente
        self.root.title(f"Socket - Cliente {self.cliente_id}")

        threading.Thread(target=self.receber_mensagens).start()

    # Funcionalidade adicional (exibir a mensagem em outro cliente)
    def receber_mensagens(self):
        # Recebe e exibe mensagens de outros clientes
        while True:
            try:
                response = self.cliente_socket.recv(1024).decode()
                if response:
                    self.exibir_resposta(f"[{self.hora}] Mensagem recebida: {response}")
            except:
                break

    def enviar_mensagem(self):
        # Envia a mensagem com o hash MD5 para o servidor
        mensagem = self.mensagem_entry.get()
        if mensagem:
            # Calcula o hash MD5 da mensagem
            hash_md5 = hashlib.md5(mensagem.encode()).hexdigest()
            mensagem_completa = f"{mensagem}|{hash_md5}"
            self.cliente_socket.send(mensagem_completa.encode())
            # Exibe a mensagem enviada na interface
            self.exibir_resposta(f"[{self.hora}] Você: {mensagem}")
            
            # Limpa o campo de texto ao enviar a mensagem
            self.mensagem_entry.delete(0, tk.END)

    def exibir_resposta(self, texto):
        # Exibe as mensagens recebidas na área de texto
        self.resposta_text.config(state='normal')
        self.resposta_text.insert(tk.END, texto + '\n')
        self.resposta_text.config(state='disabled')
        self.resposta_text.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = Cliente(root)
    root.mainloop()
