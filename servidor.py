'''Christian Matheus Oliveira Chaves
Lucas Coutinho Nascimento
Vinícius Siqueira Cardoso '''

# Importação dos módulos necessários
import socket # Módulo principal de comunicação de rede
import hashlib # Funções de hash
import os # Módulo de comandos do sistema operacional
import tkinter as tk # Módulo para gerar interface gráfica
from tkinter import scrolledtext
import threading # Módulo para gerenciamento de threads
from datetime import datetime

class Servidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Socket - Servidor")

        # Configuração do layout
        self.mensagem_text = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
        self.mensagem_text.pack(pady=5)

        self.iniciar_servidor()

    def iniciar_servidor(self):
        # Cria um socket para o servidor usando IPv4 e TCP
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associa o socket ao endereço e porta especificados
        self.servidor_socket.bind(('localhost', 12345))
        # Coloca o socket em modo de escuta, aguardando conexões de clientes
        self.servidor_socket.listen(1)
        self.adicionar_mensagem("Servidor aguardando conexões...")

        # Inicia a thread para aceitar conexões
        self.thread = threading.Thread(target=self.aceitar_conexoes)
        self.thread.start()

    # Adiciona a mensagem à janela do tkinter
    # Funcionalidade adicional
    def adicionar_mensagem(self, mensagem):
        self.mensagem_text.config(state='normal')
        self.mensagem_text.insert(tk.END, mensagem + '\n')
        self.mensagem_text.config(state='disabled')
        self.mensagem_text.yview(tk.END)

    def aceitar_conexoes(self):
        while True:
            try:
                # Aceita uma conexão de um cliente e obtém um novo socket para comunicação com o cliente
                con, ende = self.servidor_socket.accept()
                self.adicionar_mensagem(f"Conectado a: {ende}")

                while True:
                    # Recebe dados do cliente (máximo de 1024 bytes)
                    data = con.recv(1024)
                    # Se não há dados, o cliente encerrou a conexão
                    if not data:
                        break

                    # Converte os dados em string
                    data = data.decode()
                    # Verifica se a mensagem contém o caractere separador '|'
                    if '|' not in data:
                        # Se não, envia uma resposta de erro para o cliente
                        response = "Formato da mensagem inválido."
                        con.send(response.encode())
                        continue

                    # Separa a mensagem e o hash recebido
                    mensagem, hash_receb = data.split('|', 1)
                    # Calcula o hash MD5 da mensagem recebida
                    hash_calc = hashlib.md5(mensagem.encode()).hexdigest()

                    # Compara o hash recebido com o hash calculado para verificar integridade
                    if hash_receb == hash_calc:
                        response = "Mensagem recebida com sucesso e registrada em txt."
                    else:
                        response = "Falha na verificação de integridade da mensagem."

                    # Registrar a mensagem em um arquivo txt
                    # Funcionalidade adicional
                    hora = datetime.now()
                    hora_atual = hora.strftime("%H:%M:%S")
                    
                    contador = self.contar_mensagens()
                    contador += 1
                    self.atualizar_contador(contador)
                    with open('mensagens_log.txt', 'a', encoding='UTF8') as file:
                        file.write(f'--------------------{contador}--------------------\n')
                        file.write(f"Mensagem: {mensagem}\n")
                        file.write(f"Hash Recebido: {hash_receb}\n")
                        file.write(f"Hash Calculado: {hash_calc}\n")
                        file.write(f"Verificação: {'Bem-sucedida' if hash_receb == hash_calc else 'Falha'}\n")
                        file.write(f"Horário da mensagem: {hora_atual}\n")

                    # Enviar resposta ao cliente
                    con.send(response.encode())

            except Exception as e:
                # Captura e exibe qualquer erro ocorrido durante a comunicação com o cliente
                self.adicionar_mensagem(f"Erro durante a comunicação com o cliente: {e}")

    def contar_mensagens(self):
        # Lê o contador atual de mensagens do arquivo ou inicia em 0 se o arquivo não existir.
        if os.path.exists('contador.txt'):
            with open('contador.txt', 'r') as file:
                return int(file.read().strip())
        return 0

    def atualizar_contador(self, contador):
        # Atualiza o contador no arquivo
        with open('contador.txt', 'w') as file:
            file.write(str(contador))
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Servidor(root)
    root.mainloop()