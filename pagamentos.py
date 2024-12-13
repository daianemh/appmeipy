class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Ex: "Pendente", "Aprovado", "Falha"
    data = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates="pagamentos")

User.pagamentos = db.relationship('Pagamento', back_populates='user')
@app.route('/sucesso')
@login_required
def sucesso():
    valor = 100  # Aqui você pode pegar o valor real do pagamento
    novo_pagamento = Pagamento(user_id=current_user.id, valor=valor, status='Aprovado')
    db.session.add(novo_pagamento)
    db.session.commit()
    return "Pagamento realizado com sucesso!"
