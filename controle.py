from PyQt5 import uic,QtWidgets
import mysql.connector
from mysql.connector import cursor
from reportlab.pdfgen import canvas

num_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "cadastro_produtos"
)

def editar_dados():
    global num_id
    linha = lista.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_edit.show()
    
    valor_id = num_id

    tela_edit.lineEdit.setText(str(produto[0][0]))
    tela_edit.lineEdit_2.setText(str(produto[0][1]))
    tela_edit.lineEdit_3.setText(str(produto[0][2]))
    tela_edit.lineEdit_4.setText(str(produto[0][3]))
    tela_edit.lineEdit_5.setText(str(produto[0][4]))

def salvar_dados_edit():
    global num_id
    codigo = tela_edit.lineEdit_2.text()
    descricao = tela_edit.lineEdit_3.text()
    preco = tela_edit.lineEdit_4.text()
    categoria = tela_edit.lineEdit_5.text()

    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}, peco = '{}', categoria = '{}', WHERE id = {}".format(codigo,descricao,preco,categoria,num_id))
    tela_edit.close()
    lista.close()
    funcao_lista()

def excluir_dados():
    linha = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))
    
    pdf.save()
    print("PDF GERADO COM SUCESSO!")

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    
    categoria = ""

    if formulario.radioButton.isChecked():
        print("Categoria Informática foi selecionado!")
        categoria = "Informática"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Alimentos foi selecionado!")
        categoria = "Alimentos"
    else:
        print("Categoria Eletronicos foi selecionado!")
        categoria = "Eletronicos"

    print("Codigo: ", linha1)
    print("Descricao: ", linha2)
    print("Preco: ", linha3)
    
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def funcao_lista():
    lista.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    lista.tableWidget.setRowCount(len(dados_lidos))
    lista.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista.tableWidget.setItem(i, j, 
            QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
lista = uic.loadUi("lista_de_produtos.ui")
tela_edit = uic.loadUi("menu_edit.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(funcao_lista)
lista.pushButton.clicked.connect(gerar_pdf)
lista.pushButton_2.clicked.connect(excluir_dados)
lista.pushButton_3.clicked.connect(editar_dados)
tela_edit.pushButton.clicked.connect(salvar_dados_edit)

formulario.show()
app.exec()