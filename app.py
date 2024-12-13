from flask import Flask, jsonify, render_template, request, redirect, url_for
from sqlalchemy import Transaction
from models import db, Client

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Rota para a página inicial
@app.route('/')
def home():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

# Rota para adicionar um cliente
@app.route('/add', methods=['POST'])
def add_client():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    new_client = Client(name=name, email=email, phone=phone)
    db.session.add(new_client)
    db.session.commit()

    return redirect(url_for('home'))

# Rota para deletar um cliente
@app.route('/delete/<int:id>')
def delete_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
# Rota para exibir todos os produtos
@app.route('/estoque')
def estoque():
    products = Product.query.all()
    return render_template('estoque.html', products=products)

# Rota para adicionar um produto
@app.route('/estoque/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    min_quantity = int(request.form.get('min_quantity'))

    new_product = Product(name=name, quantity=quantity, price=price, min_quantity=min_quantity)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('estoque'))

# Rota para atualizar a quantidade de um produto
@app.route('/estoque/update/<int:id>', methods=['POST'])
def update_product(id):
    product = Product.query.get(id)
    product.quantity = int(request.form.get('quantity'))
    db.session.commit()
    return redirect(url_for('estoque'))

# Rota para deletar um produto
@app.route('/estoque/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('estoque'))
# Rota para buscar produtos no estoque
@app.route('/estoque/buscar', methods=['GET'])
def buscar_produto():
    query = request.args.get('query')  # Captura o termo de busca
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        products = Product.query.all()
    return render_template('estoque.html', products=products)
import csv
from flask import Response

# Rota para exportar estoque como CSV
@app.route('/estoque/exportar')
def exportar_estoque():
    products = Product.query.all()

    # Gerar CSV em memória
    def generate():
        data = ['Nome,Quantidade,Preço,Estoque Mínimo\n']
        for product in products:
            data.append(f'{product.name},{product.quantity},{product.price},{product.min_quantity}\n')
        yield ''.join(data)

    # Retornar CSV como resposta
    return Response(generate(), mimetype='text/csv', headers={
        'Content-Disposition': 'attachment;filename=estoque.csv'
    })
from datetime import datetime

# Página financeira
@app.route('/financeiro')
def financeiro():
    transactions = Transaction.query.all()
    saldo = sum(t.amount for t in transactions)  # Calcula o saldo total
    return render_template('financeiro.html', transactions=transactions, saldo=saldo)

# Adicionar uma transação
@app.route('/financeiro/add', methods=['POST'])
def add_transaction():
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')

    transaction = Transaction(description=description, amount=amount, date=date)
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('financeiro'))

# Deletar uma transação
@app.route('/financeiro/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('financeiro'))
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

# Inicializando o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'
@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        novo_fornecedor = Fornecedor(nome=nome, contato=contato)
        db.session.add(novo_fornecedor)
        db.session.commit()
        return redirect(url_for('fornecedores'))
    
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores.html', fornecedores=fornecedores)
import mercadopago
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SECRET_KEY'] = 'secretkey'

# Configuração do Mercado Pago
mp = mercadopago.MP("CLIENT_ID", "CLIENT_SECRET")

db = SQLAlchemy(app)

# Inicializando o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/pagamento', methods=['POST'])
def pagamento():
    valor = float(request.form['valor'])

    # Criação de preferência de pagamento (exemplo de pagamento via boleto)
    preference_data = {
        "items": [
            {
                "title": "Produto X",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }
        ],
        "payment_methods": {
            "excluded_payment_types": [
                {"id": "ticket"}
            ],
            "installments": 1
        },
        "back_urls": {
            "success": url_for('sucesso', _external=True),
            "failure": url_for('falha', _external=True),
            "pending": url_for('pendente', _external=True)
        },
        "auto_return": "approved"
    }

    preference = mp.preferences.create(preference_data)
    preference_url = preference['response']['init_point']

    return redirect(preference_url)
@app.route('/sucesso')
def sucesso():
    return "Pagamento realizado com sucesso!"

@app.route('/falha')
def falha():
    return "O pagamento falhou. Tente novamente."

@app.route('/pendente')
def pendente():
    return "O pagamento está pendente. Aguarde a confirmação."
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Criando o modelo de usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais incorretas. Tente novamente.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar se o usuário já existe
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Nome de usuário ou email já existe.')
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso. Faça login.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.username}! Você está logado."
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')
        
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Nome de usuário ou email já existe.')
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso. Faça login.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais incorretas. Tente novamente.')
    return render_template('login.html')
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect('db/meu_banco_de_dados.db')
    return conn

# Página inicial
@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        # Aqui você pode adicionar a lógica de autenticação
        return redirect(url_for('index'))
    return render_template('login.html')

# Criar um produto (exemplo de inserção no banco)
@app.route('/criar_produto', methods=['POST'])
def criar_produto():
    nome = request.form['nome']
    preco = request.form['preco']
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Rodar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

import requests

def listar_produtos_mercadolivre():
    url = "https://api.mercadolibre.com/users/me"
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    }
    response = requests.get(url, headers=headers)
    produtos = response.json()
    print(produtos)

listar_produtos_mercadolivre()

import boto3

def backup_para_s3(file_path, bucket_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, 'backup.db')
    print("Backup realizado com sucesso!")

# Exemplo de uso
backup_para_s3('db/meu_banco_de_dados.db', 'meu-bucket-s3')

from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    print('Mensagem recebida: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def enviar_email(destinatario, assunto, conteudo):
    sg = sendgrid.SendGridAPIClient(api_key='YOUR_API_KEY')
    from_email = Email("seu_email@dominio.com")
    to_email = To(destinatario)
    subject = assunto
    content = Content("text/plain", conteudo)

    mail = Mail(from_email, to_email, subject, content)

    response = sg.send(mail)
    print(response.status_code, response.body, response.headers)

# Enviar um e-mail
enviar_email("cliente@dominio.com", "Sua promoção", "Confira nossa oferta especial!")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed'

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(description=data['description'], due_date=data['due_date'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201
class FinancialRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    record_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/financial', methods=['POST'])
def add_financial_record():
    data = request.json
    record = FinancialRecord(amount=data['amount'], record_type=data['record_type'])
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Financial record added'}), 201
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='sales')
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/sales', methods=['POST'])
def register_sale():
    data = request.json
    product = Product.query.get(data['product_id'])
    if product.quantity < data['quantity']:
        return jsonify({'message': 'Not enough stock available'}), 400
    product.quantity -= data['quantity']
    sale = Sale(product_id=data['product_id'], quantity=data['quantity'], total_price=data['quantity'] * product.price)
    db.session.add(sale)
    db.session.commit()
    return jsonify({'message': 'Sale registered successfully'}), 201

def calcular_imposto(atividade, receita_mensal):
    if atividade == "comercio":
        imposto = 60.00  # Valor fixo para o comércio
    elif atividade == "industria":
        imposto = 80.00  # Valor fixo para a indústria
    elif atividade == "servico":
        imposto = 50.00  # Valor fixo para serviços
    else:
        imposto = 0.00

    return imposto

# Exemplo de uso
atividade = "comercio"
receita_mensal = 5000.00
imposto = calcular_imposto(atividade, receita_mensal)
print(f"O imposto mensal é: R${imposto}")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'
@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.json
        new_product = Product(name=data['name'], description=data['description'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    
    products = Product.query.all()
    return jsonify([{'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products])
