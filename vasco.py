#código Misto

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
jogadores = {}
pontos = 0
Janela = tk.Tk()
Janela.title("Damas")
nome_vencedor = ""

def obter_ultimo_nome_scoreboard():
    with open("scoreboard.txt", "r") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            nome_vencedor = last_line.split(":")[0].strip()
            return nome_vencedor

def abrejogo():
    Janela.iconify()
    jogo = JogoDeDamas()
    jogo.janela.mainloop()

def registro(usuario):
    if not usuario or len(usuario) == 1:
        popup = tk.Toplevel()
        popup.title("ERROR!")
        popup.geometry("300x100")
        label = tk.Label(popup, text="Nome de usuário inválido,tente novamente.")
        label.pack(pady=20)
        button = tk.Button(popup, text="Ok!", command=popup.destroy)
        button.pack()
        return
    

    with open("scoreboard.txt", "a+") as f:
        lines = f.readlines()
        for line in lines:
            if usuario in line:
                print(f"Bem-vindo de volta, {usuario}!")
                return
        f.write(f"{usuario}: {pontos}\n")
        print(f"Bem-vindo, {usuario}! Você foi adicionado ao Scoreboard!.")

def atualizar_pontuacao(nome, pontos):
    with open("scoreboard.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if nome in line:
                line_parts = line.split(":")
                line_parts[1] = str(pontos)
                line = ":".join(line_parts)
            f.write(line)
        f.truncate()
        
def mostrar_jogadores():
    with open("scoreboard.txt", "r") as f:
        conteudo = f.read()

    # nova janela para exibir os jogadores
    janela_jogadores = tk.Toplevel(Janela)
    janela_jogadores.title("Jogadores")

    # exibição dos jogadores
    text_widget = tk.Text(janela_jogadores)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # insere conteudo
    text_widget.insert(tk.END, conteudo)

def exibir_regras():
    popup = tk.Toplevel()
    popup.title("REGRAS")
    label = tk.Label(popup, text="""

        1 - Os jogadores podem selecionar uma peça para movimentar clicando nela no tabuleiro.

        2 - Uma vez selecionada a peça, o jogador pode movê-la para uma casa vazia adjacente diagonalmente.

        3 - Se a peça selecionada estiver pulando sobre uma peça adversária, ela pode realizar um movimento de captura.

        4 - Se uma peça atinge a última linha do tabuleiro adversário, ela é promovida a uma dama.

        5 - Se a peça selecionada for uma dama, ela pode se mover em qualquer direção diagonal.

        6 - Após cada movimento válido, o tabuleiro é atualizado e o próximo jogador pode fazer sua jogada.""")

    label.pack(pady=20)
    button = tk.Button(popup, text="Ok!", command=popup.destroy)
    button.pack()

def quit_game():
        res = tk.messagebox.askyesno('Confirmar saída', 'Você quer realmente sair?')
        if res:
            Janela.quit()
            Janela.destroy()

entrada = tk.Entry(Janela)
entrada.pack()

botão_Registro = tk.Button(Janela, text="Registrar Jogador", command=lambda: registro(entrada.get()))
botão_Registro.pack()

botão_Display = tk.Button(Janela, text="High Scores", command=mostrar_jogadores)
botão_Display.pack()

botão_Regras = tk.Button(Janela, text="Regras", command=exibir_regras)
botão_Regras.pack()

Botão_PvP = tk.Button(Janela, text="PvP", command=abrejogo)
Botão_PvP.pack()

botao_sair = tk.Button(Janela, text="Sair do Jogo", command=quit_game)
botao_sair.pack()

class JogoDeDamas:
    def __init__(self):
        # Criar janela
        self.janela = tk.Toplevel()
        self.janela.title("Jogo de Damas")

        self.botao_voltar = tk.Button(self.janela, text="Voltar", command=self.voltar_menu)
        self.botao_voltar.pack()

        # Criar um canvas para desenhar o tabuleiro
        self.canvas = tk.Canvas(self.janela, width=1024, height=800)
        self.canvas.pack()

        # Carregar as imagens das peças
        self.peca_jogador1 = ImageTk.PhotoImage(Image.open("black_p.png").resize((85, 85)))
        self.peca_jogador2 = ImageTk.PhotoImage(Image.open("3.png").resize((82, 82)))
        self.imagem_tabuleiro = ImageTk.PhotoImage(Image.open("1.png").resize((800, 800)))
        self.imagem_coroa = ImageTk.PhotoImage(Image.open("coroa.png").resize((60, 60)))

        # Inicializar o turno 
        self.turno = 1

        # Armazena a última peça que comeu outra
        self.ultima_peca_comer = None

        # Inicializa o tabuleiro
        self.tabuleiro = [[0]*8 for _ in range(8)]
        for x in range(8):
            for y in range(8):
                if (x+y) % 2 != 0:
                    if x < 3:
                        self.tabuleiro[x][y] = {'Jogador':1,'Dama':False}
                    elif x > 4:
                        self.tabuleiro[x][y] = {'Jogador':2,'Dama':False}

        # Adiciona manipulador de eventos de clique ao canvas
        self.peca_selecionada = None
        self.canvas.bind("<Button-1>", self.seleciona_peca)


        # Desenha o tabuleiro
        self.desenha_tabuleiro()

    def desenha_tabuleiro(self):
        self.canvas.create_image(0, 0, image=self.imagem_tabuleiro, anchor="nw")
        for x in range(8):
            for y in range(8):
                # Desenha as peças
                piece = self.tabuleiro[x][y]
                if piece != 0:
                    image = self.peca_jogador1 if piece['Jogador'] == 1 else self.peca_jogador2
                    self.canvas.create_image(y*100+50, x*100+50, image=image)

                    # Verifica se a peça é uma dama e desenha a coroa
                    if piece['Dama']:
                        self.canvas.create_image(y*100+50, x*100+50, image=self.imagem_coroa)

                # Desenha o destaque na peça selecionada
                if self.peca_selecionada == (x, y):
                    self.canvas.create_oval(y*100+10, x*100+10, (y+1)*100-10, (x+1)*100-10, outline="yellow", width=3)

                if self.peca_selecionada:
                    for movimento in self.calcula_movimentos_possiveis(*self.peca_selecionada):
                        self.canvas.create_oval(movimento[1]*100+35, movimento[0]*100+35, (movimento[1]+1)*100-35, (movimento[0]+1)*100-35, fill="blue",outline='gray',width=1)

    def contar_pecas(self):
        pecas_jogador1 = 0
        pecas_jogador2 = 0

        for x in range(8):
            for y in range(8):
                if self.tabuleiro[x][y] != 0:
                    if self.tabuleiro[x][y]['Jogador'] == 1:
                        pecas_jogador1 += 1
                    else:
                        pecas_jogador2 += 1

        return pecas_jogador1, pecas_jogador2

    def verifica_vencedor(self):
        pecas_jogador1, pecas_jogador2 = self.contar_pecas()

        if pecas_jogador1 == 0:
            return 2
        elif pecas_jogador2 == 0:
            return 1
        else:
            return None

    def realizar_jogada(self, jogada):
        origem, destino = jogada
        pecas_jogador1, pecas_jogador2 = self.contar_pecas()

        if self._eh_movimento_valido(origem, destino):
            peca = self.tabuleiro[origem[0]][origem[1]]
            self.tabuleiro[origem[0]][origem[1]] = 0
            self.tabuleiro[destino[0]][destino[1]] = peca
            print(f'Jogada realizada de {origem} para {destino}.')

            # Contagem de peças após a jogada
            pecas_jogador1, pecas_jogador2 = self.contar_pecas()
            print(f'Jogador 1: {pecas_jogador1} peças. Jogador 2: {pecas_jogador2} peças.')

            # Verifica se algum jogador venceu
            vencedor = self.verifica_vencedor()
            if vencedor:
                print(f'Fim do jogo! O vencedor é o jogador {vencedor}.')

            return True
        else:
            print('Movimento inválido.')
            return False



    def seleciona_peca(self, event):
        # Calcula a casa do tabuleiro onde o clique ocorreu
        casa_x, casa_y = event.y // 100, event.x // 100


        # Se uma peça estiver selecionada e o jogador clicar em um quadrado vazio
        if self.peca_selecionada and self.tabuleiro[casa_x][casa_y] == 0:
            # Calcula a diferença entre a peça selecionada e a casa do tabuleiro onde o clique ocorreu
            dx, dy = casa_x - self.peca_selecionada[0], casa_y - self.peca_selecionada[1]

            # Pega a peça selecionada
            piece = self.tabuleiro[self.peca_selecionada[0]][self.peca_selecionada[1]]
            if piece['Dama'] == True and dy in (-1, 1):
                self.tabuleiro[casa_x][casa_y] = piece
                self.tabuleiro[self.peca_selecionada[0]][self.peca_selecionada[1]] = 0
                self.peca_selecionada = None

            # Verifica se o movimento é válido
            elif piece['Jogador'] == 1 and dx == 1 and dy in (-1, 1) or \
            piece['Jogador'] == 2 and dx == -1 and dy in (-1, 1):
                # Verificando a promoção para Dama
                if piece['Jogador'] == 1 and casa_x == 7:
                    piece['Dama'] = True
                elif piece['Jogador'] == 2 and casa_x == 0:
                    piece['Dama'] = True

                # Move a peça
                self.tabuleiro[casa_x][casa_y] = piece
                self.tabuleiro[self.peca_selecionada[0]][self.peca_selecionada[1]] = 0

                # Desmarca a peça selecionada
                self.peca_selecionada = None

                # Se a peça selecionada está pulando sobre uma peça adversária
            if abs(dx) == 2 and abs(dy) == 2:
                # Calcula a posição da peça que está sendo pulada
                meio_x, meio_y = self.peca_selecionada[0] + dx // 2, self.peca_selecionada[1] + dy // 2

                # Se a peça no meio é uma peça adversária
                if self.tabuleiro[meio_x][meio_y] != 0 and self.tabuleiro[meio_x][meio_y] != piece:
                    # Move a peça selecionada
                    self.tabuleiro[casa_x][casa_y] = piece
                    # Verificando a promoção para Dama
                    if piece['Jogador'] == 1 and casa_x == 7:
                        piece['Dama'] = True
                    elif piece['Jogador'] == 2 and casa_x == 0:
                        piece['Dama'] = True
                    self.tabuleiro[meio_x][meio_y] = 0
                    self.tabuleiro[self.peca_selecionada[0]][self.peca_selecionada[1]] = 0
                    self.peca_selecionada = None

            if abs(dx) == 2 and abs(dy) == 2:
                self.ultima_peca_comer = (casa_x, casa_y)

                # Se a peça que comeu não tem mais movimentos de captura, muda o turno
                if len(self.calcula_movimentos_possiveis(casa_x, casa_y)) == 0:
                    self.turno = 3 - self.turno
                    self.ultima_peca_comer = None
            else:
                # Se o movimento não foi uma captura, muda o turno
                self.turno = 3 - self.turno
                self.ultima_peca_comer = None


            print(self.turno)
            
            self.desenha_tabuleiro()
            self.verificar_jogo()

        elif self.tabuleiro[casa_x][casa_y] != 0:
            # Seleciona a peça se for a vez do jogador da peça e
            # (não é a peça que comeu na última jogada ou é a peça que comeu e tem movimentos válidos)
            if self.tabuleiro[casa_x][casa_y]['Jogador'] == self.turno and \
            (self.ultima_peca_comer is None or
            self.ultima_peca_comer == (casa_x, casa_y) and
            len(self.calcula_movimentos_possiveis(casa_x, casa_y)) > 0):
                self.peca_selecionada = (casa_x, casa_y)
                self.desenha_tabuleiro()

    def verifica_vencedor(self):
        pecas_jogador1, pecas_jogador2 = self.contar_pecas()
        if pecas_jogador1 == 0:
            return 2
        elif pecas_jogador2 == 0:
            return 1
        return None
    def contar_pecas(self):
        pecas_jogador1 = sum(1 for linha in self.tabuleiro for peca in linha if peca != 0 and peca['Jogador'] == 1)
        pecas_jogador2 = sum(1 for linha in self.tabuleiro for peca in linha if peca != 0 and peca['Jogador'] == 2)
        return pecas_jogador1, pecas_jogador2
    
    def obter_ultimo_nome_scoreboard():
        with open("scoreboard.txt", "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                nome_vencedor = last_line.split(":")[0].strip()
                return nome_vencedor
            else:
                return "Nome não encontrado"

    def exibir_resultados_jogo(nome_vencedor, pontos):
        popup = tk.Toplevel()
        popup.title("Resultado do Jogo")
    
        label_vencedor = tk.Label(popup, text=f'Fim do jogo! O vencedor é o {nome_vencedor}.')
        label_vencedor.pack(pady=10)
    
        label_pontos = tk.Label(popup, text=f'Pontos do jogador vencedor: {pontos}')
        label_pontos.pack(pady=10)

    def verificar_jogo(self):
        pecas_jogador1, pecas_jogador2 = self.contar_pecas()
        print(f'Jogador 1: {pecas_jogador1} peças. Jogador 2: {pecas_jogador2} peças.')
        if self.calcula_movimentos_jogador() == 0:
            print(f'Fim do jogo! O vencedor é o jogador {3 - self.turno}, pois o jogador {self.turno} não tem movimentos possíveis.')
        
        nome_vencedor = obter_ultimo_nome_scoreboard()
        vencedor = self.verifica_vencedor()
        if vencedor is not None:
            pontos = pecas_jogador1*300
            atualizar_pontuacao(nome_vencedor, pontos)
            if vencedor == 1:

                popup = tk.Toplevel()
                popup.title("Resultado:" )
                popup.geometry("300x100")
                label = tk.Label(popup, text=f'Fim do jogo!\nO vencedor é {nome_vencedor}.\nSeus pontos foram: {pontos}',justify='center', wraplength=250)
                label.pack(pady=20)
                button = tk.Button(popup, text="Ok!", command=popup.destroy)
                button.pack()
    def calcula_movimentos_jogador(self):
        total_movimentos = 0
        for x in range(8):
            for y in range(8):
                if self.tabuleiro[x][y] != 0 and self.tabuleiro[x][y]['Jogador'] == self.turno:
                    total_movimentos += len(self.calcula_movimentos_possiveis(x, y))
        return total_movimentos

    def calcula_movimentos_possiveis(self, x, y):
        movimentos = []
        piece = self.tabuleiro[x][y]
        if piece['Dama'] == False:
            for dx, dy in [(2, 2),(2, -2),(-2, -2),(-2, 2),(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                novo_x, novo_y = x + dx, y + dy
                if 0 <= novo_x < 8 and 0 <= novo_y < 8 and self.tabuleiro[novo_x][novo_y] == 0:
                    if (piece['Jogador'] == 1 and dx == 1) or (piece['Jogador'] == 2 and dx == -1):
                        movimentos.append((novo_x, novo_y))

                    elif isinstance(self.tabuleiro[x + dx // 2][y + dy // 2], dict) and (piece['Jogador'] == 1 and abs(dx) == 2 and self.tabuleiro[x + dx // 2][y + dy // 2]['Jogador'] != 1) or \
                    (piece['Jogador'] == 2 and abs(dx) == 2 and isinstance(self.tabuleiro[x + dx // 2][y + dy // 2], dict) and self.tabuleiro[x + dx // 2][y + dy // 2]['Jogador'] != 2):
                        movimentos.append((novo_x, novo_y))
        elif piece['Dama']==True:
            for dx, dy in [(2, 2),(2, -2),(-2, -2),(-2, 2),(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                novo_x, novo_y = x + dx, y + dy
                if 0 <= novo_x < 8 and 0 <= novo_y < 8 and self.tabuleiro[novo_x][novo_y] == 0:
                    if (piece['Jogador'] == 1 and dx == 1 or dx == -1) or (piece['Jogador'] == 2 and dx == 1 or dx == -1):
                        movimentos.append((novo_x, novo_y))

                    elif isinstance(self.tabuleiro[x + dx // 2][y + dy // 2], dict) and (piece['Jogador'] == 1 and abs(dx) == 2 and self.tabuleiro[x + dx // 2][y + dy // 2]['Jogador'] != 1) or \
                    (piece['Jogador'] == 2 and abs(dx) == 2 and isinstance(self.tabuleiro[x + dx // 2][y + dy // 2], dict) and self.tabuleiro[x + dx // 2][y + dy // 2]['Jogador'] != 2):
                        movimentos.append((novo_x, novo_y))
        print(movimentos)
        if self.ultima_peca_comer == (x, y):
            # Se a peça é a peça que comeu na última jogada, remove os movimentos que não são capturas
            movimentos = [(nx, ny) for nx, ny in movimentos if abs(nx - x) == 2 and abs(ny - y) == 2]



        return movimentos
    def voltar_menu(self):
        self.janela.destroy()
        Janela.deiconify()

Janela.mainloop()