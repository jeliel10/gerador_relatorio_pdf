from tkinter import *
from tkinter import ttk

# Bibliotecas para geração de PDF.
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image

import webbrowser  # Importação para chamar o navegador.
import sqlite3

root = Tk()


class Relatorios():
    # Essa primeira função é responsavel por exibir e salvar o arquivo.
    def printCliente(self):  # Essa função serve para chamar o navegador padrão e aparecer o nosso PDF.
        webbrowser.open(
            "cliente.pdf")  # aqui ele vai criar um arquivo PDF na pasta onde o projeto estiver. OBS: Eu posso colocar um camnho aqui também.

    # Essa segunda função é a responsavel por montar o PDF.
    def geraRelatCliente(self):  # Função para gerar o relatorio
        self.c = canvas.Canvas("cliente.pdf")  # Variavel do arquivo PDF. Coloca o mesmo nome que ta na função anterior.

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold",
                       24)  # Colocando uma fonte para esse relatorio. OBS: o reportlab tem varias fontes disponiveis.
        self.c.drawString(200,  # Essa numero é a posição da esquerda para direita   #Vai desenhar uma String na tela.
                          790,  # Esse numero é a posição de cima para baixo
                          'Ficha do Cliente')

        # Esse bloco de código vai criar os atributos em negrito.
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, "Nome: ")
        self.c.drawString(50, 640, "Telefone: ")
        self.c.drawString(50, 610, "Cidade: ")

        # Esse bloco de código vai colocar as informações sem estarem em negrito.
        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 640, self.telefoneRel)
        self.c.drawString(150, 610, self.cidadeRel)

        # Esse bloco de código são responsaveis por criar os Retangulos no PDF.
        self.c.rect(20, 740, 550, 100, fill=False, stroke=True) # Retangulo do Ficha Cliente
        self.c.rect(20,  # Esse numero é a posição de onde ele vai começar, da esquerda para direita.
                    600,  # Esse numero é a posição inicial dele, de baixo para cima.
                    550,  # Esse numero é o comprimento até onde ele vai, da esquerda para direita.
                    120,  # Esse numero é o tamanho do retangulo
                    fill=False,  # O Fill é o que vai dizer se vai ser preenchido ou não por dentro.
                    stroke=True  # O Stroke é o que vai dizer se vai as bordas vão ser preenchidas ou não.
                    )                                           # Retangulo das informações do Cliente.

        self.c.showPage()  # Vai chamar a pagina PDF.
        self.c.save()  # Vai salvar a pagina PDF.
        self.printCliente()


class Functions():
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clitens.bd")
        print("Conectando ao banco de dados")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do banco de dados")

    def montaTabelas(self):
        self.conecta_bd()

        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                name_cliente VARCHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade VARCHAR(40)
            );
        """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""
            INSERT INTO clientes (name_cliente, telefone, cidade)
            VALUES (?, ?, ?)
        """, (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" 
            SELECT cod, name_cliente, telefone, cidade FROM clientes
            ORDER BY name_cliente ASC;
        """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):  # sempre que uma função for fazer algo, é necessario colocar esse event.
        self.limpar_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
            UPDATE clientes SET name_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())      # Vai limpar a lista

        self.nome_entry.insert(END, '%')    # Quando eu for buscar o nome do cliente, é necessario inserir um % depois do nome. Essa linha vai colocar ele automaticamente. Essa porcentagem é para mostrar todos os clientes que tem aquele nome que eu coloquei
        nome = self.nome_entry.get()
        self.cursor.execute("""
            SELECT cod, name_cliente, telefone, cidade FROM clientes
            WHERE name_cliente LIKE '%s' ORDER BY name_cliente ASC;
        """ % nome)
        buscanomeCli = self.cursor.fetchall()   # Vai fechar a pesquisa para usar no For.
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()


class Application(Functions, Relatorios):

    # Variaveis Cores
    cor_de_fundo = '#dfe3ee'
    cor_de_fundo_tela = '#1e3743'
    borda_frames = '#759fe6'

    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame_2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background=self.cor_de_fundo_tela)  # Cor de fundo. Pode ser uma imagem tbm.
        self.root.geometry("700x500")  # dimensões iniciais da tela.
        self.root.resizable(True, True)  # se vai permitir que a tela seja expandida ou reduzida.
        self.root.maxsize(width=900, height=700)  # tamanho maximo que a tela pode ser expandida.
        self.root.minsize(width=500, height=400)  # tamanho minimo que a tela pode ser diminuida.

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg=self.cor_de_fundo,
                             highlightbackground=self.borda_frames, highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg=self.cor_de_fundo,
                             highlightbackground=self.borda_frames, highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame_1(self):
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg='black', highlightbackground= 'gray',
                        highlightthickness= 3)
        self.canvas_bt.place(relx= 0.19, rely= 0.09, relwidth= 0.3, relheight= 0.19)

        ## Criação da Label e Entrada do código
        self.lb_codigo = Label(self.frame_1, text="Código", bg=self.cor_de_fundo, fg='blue')
        self.lb_codigo.place(relx=0.05, rely=0.05)  # posição da label na tela.

        self.codigo_entry = Entry(self.frame_1, bg=self.cor_de_fundo)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        ## Criação da Label e Entrada do Nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg=self.cor_de_fundo, fg='blue')
        self.lb_nome.place(relx=0.05, rely=0.35)  # posição da label na tela.

        self.nome_entry = Entry(self.frame_1, bg=self.cor_de_fundo)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

        ## Criação da Label e Entrada do Telefone
        self.lb_telefone = Label(self.frame_1, text="Telefone", bg=self.cor_de_fundo, fg='blue')
        self.lb_telefone.place(relx=0.05, rely=0.6)  # posição da label na tela.

        self.telefone_entry = Entry(self.frame_1, bg=self.cor_de_fundo)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        ## Criação da Label e Entrada do Cidade
        self.lb_cidade = Label(self.frame_1, text="Cidade", bg='#dfe3ee', fg='blue')
        self.lb_cidade.place(relx=0.5, rely=0.6)  # posição da label na tela.

        self.cidade_entry = Entry(self.frame_1, bg=self.cor_de_fundo)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.35)

        ### Criação do botão Limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar",
                                bd=5,  # estilo da borda
                                bg='dodger blue',  # cor de fundo do botão
                                fg='white',  # cor do texto
                                font=('arial', 8, 'bold'), command=self.limpar_tela)  # fonte do texto
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão Novo
        self.bt_novo = Button(self.frame_1, text="Novo",
                              bd=5,
                              bg='dodger blue',
                              fg='white',
                              font=('arial', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão Apagar
        self.bt_buscar = Button(self.frame_1, text="Apagar",
                                bd=5,
                                bg='dodger blue',
                                fg='white',
                                font=('arial', 8, 'bold'), command=self.deleta_cliente)
        self.bt_buscar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão Alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar",
                                 bd=5,
                                 bg='dodger blue',
                                 fg='white',
                                 font=('arial', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botão Buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar",
                                bd=5,
                                bg='dodger blue',
                                fg='white',
                                font=('arial', 8, 'bold'), command=self.busca_cliente)  # bold é para deixar em negrito
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

    def lista_frame_2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")  # Nome do cabeçalho de cada coluna
        self.listaCli.heading('#1', text="Código")
        self.listaCli.heading('#2', text="Nome")
        self.listaCli.heading('#3', text="Telefone")
        self.listaCli.heading('#4', text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')  # Barra de rolagem
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = Menu(menubar)  # Criando as 2 instancias de Menus
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()  # Função para sair do sistema.

        menubar.add_cascade(label="Opções", menu=filemenu)  # Menu de Opções
        menubar.add_cascade(label="Relatorios", menu=filemenu2)  # Menu de Sobre

        filemenu.add_command(label="Sair", command=Quit)  # Dentro do Menu de Opções, vai poder sair do sistema
        filemenu.add_command(label="Limpar Tela",  # Dentro do Menu de Sobre, vai poder limpar a tela.
                             command=self.limpar_tela)

        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelatCliente)


Application()
