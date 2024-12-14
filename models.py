from flask_sqlalchemy import SQLAlchemy

# Definir o banco de dados
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Verificar o login do usuário
    @staticmethod
    def verify_login(db, email, password):
        user = User.query.filter_by(email=email, password=password).first()
        return user

    # Criar um novo usuário
    @staticmethod
    def create_user(db, email, password):
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
