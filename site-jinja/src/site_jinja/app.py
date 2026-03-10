from flask import Flask, render_template, request
from datetime import datetime


# Criando a aplicação Flask
app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

#criando variaveis
lista_pedidos = []
lista_pedidos = []
pedidos_balcao = []

# Criando uma ROTA (o endereço do site)
@app.route("/")
def home():
    # Aqui o Python prepara os dados
    titulo_site = "Aula de Flask - 3º Ano"
    
    # O Python "renderiza" (desenha) o HTML e envia as variáveis
    return render_template("index.html", titulo=titulo_site)

@app.route("/contato")
def sobre():
    return render_template("contato.html", titulo="Contato")


@app.route("/receber-pedido", methods=['POST'])
def receber_pedido():
    # O objeto 'request.form' funciona como um dicionário
    # Ele pega os dados pelo 'name' que definimos no HTML
    
    prato_escolhido = request.form.get('nome_do_prato')
    mesa_cliente = request.form.get('numero_mesa')
    
    # Vamos mostrar no terminal do VS Code para o programador ver
    print(f"NOVO PEDIDO! Mesa: {mesa_cliente} | Prato: {prato_escolhido}")
    lista_pedidos.append({"mesa": mesa_cliente, "prato": prato_escolhido})
    # Retorna uma confirmação para o usuário
    return f"""
    <h1>Pedido Recebido! ✅</h1>
    <p>A cozinha está preparando um <strong>{prato_escolhido}</strong> para a mesa <strong>{mesa_cliente}</strong>.</p>
    <a href='/'>Voltar</a>
    """
#pedidos recebiddos
@app.route("/pedidos-recebidos")
def pedidos_recebidos():
    existe_pedidos = len(lista_pedidos) > 0
    data = datetime.now()
    return render_template("cozinha.html", pedidos=lista_pedidos,existe_pedidos=existe_pedidos, hoje=data)

#atualizar pedido
@app.route("/atualizar_pedidos", methods=["GET", "POST"])
def atualizar_pedidos():

    if request.method == "POST":
        mesa = request.form.get("mesa")
        novo_prato = request.form.get("novo_prato")

        for pedido in lista_pedidos:
            if pedido["mesa"] == mesa:
                pedido["prato"] = novo_prato

    existe_pedidos = len(lista_pedidos) > 0
    data = datetime.now()

    return render_template(
        "atualizar.html",
        pedidos=lista_pedidos,
        existe_pedidos=existe_pedidos,
        hoje=data
    )
    
@app.route("/balcao", methods=["GET","POST"])
def balcao():

    if request.method == "POST":
        mesa = request.form.get("mesa")

        for pedido in lista_pedidos:
            if pedido["mesa"] == mesa:
                pedidos_balcao.append(pedido)
                lista_pedidos.remove(pedido)
                break

    return render_template("balcao_pedidos.html", pedidos=pedidos_balcao)

@app.template_filter('datetime_format')
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

# Rodando o servidor
if __name__ == "__main__":
    app.run(debug=True) # debug=True faz o site atualizar sozinho quando salvamos
