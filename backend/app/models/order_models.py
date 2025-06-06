from app.config import db

class Comanda(db.Model):
    __tablename__ = 'comandas'
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.Integer, nullable=False)
    data_abertura = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('aberta', 'fechada', 'cancelada', name='status_enum'), default='aberta', nullable=False)
    total_pago = db.Column(db.Float, default=0.0)
    
    pagamentos = db.relationship('Pagamento', backref='comanda', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'mesa': self.mesa,
            'data_abertura': self.data_abertura,
            'status': self.status
        }

class ComandaNaoEncontrada(Exception):
    pass

def criar_comandas(mesa, data_abertura):
    # Verifica se a mesa já está ocupada
    mesa_existente = Comanda.query.filter_by(mesa=mesa, status='aberta').first()
    if mesa_existente:
        return {'error': 'Mesa já ocupada'}, 400
    # Cria uma nova comanda
    nova_comanda = Comanda(mesa=mesa, data_abertura=data_abertura)
    db.session.add(nova_comanda)    
    db.session.commit()
    return nova_comanda.to_dict()

def listar_comanda():
    comanda = Comanda.query.all()
    print(comanda)
    #return {'error': 'Comanda fechada'}, 400
    return [c.to_dict() for c in comanda if c.status != 'fechada' and c.status != 'cancelada']

def comanda_por_id(id_order):
    comanda = Comanda.query.get(id_order)
    if not comanda:
        raise ComandaNaoEncontrada
    return comanda.to_dict()

def atualizar_comanda(id_order, novos_dados):
    comanda = Comanda.query.get(id_order)
    if not comanda:
        raise ComandaNaoEncontrada
    comanda.mesa = novos_dados.get('mesa')
    comanda.data_abertura = novos_dados.get('data_abertura')
    comanda.status = novos_dados.get('status')
    db.session.commit()
    return comanda.to_dict()

