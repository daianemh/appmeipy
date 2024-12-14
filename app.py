from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco_de_dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Página inicial (Login)
@app.route('/')
def index():
    return render_template('login.html')

# Página de login (POST)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Verificar se os dados do usuário estão corretos no banco de dados
    user = User.verify_login(db, email, password)
    
    if user:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

# Página home (após login)
@app.route('/home')
def home():
    return render_template('home.html')

# Página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Criar novo usuário no banco de dados
        User.create_user(db, email, password)
        return redirect(url_for('index'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
