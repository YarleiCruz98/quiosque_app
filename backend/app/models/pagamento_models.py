from app.config import db

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    troco = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.DateTime, default=db.func.now())