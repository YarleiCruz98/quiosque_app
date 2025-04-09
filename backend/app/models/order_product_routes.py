from app.config import db
from app.models.order_models import Comanda

class ComandaProduto(db.Model):
    __tablename__ = 'comanda_produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id', ondelete='CASCADE'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)  # Descrição opcional do produto na comanda
    # Relacionamentos
    comanda = db.relationship('Comanda', backref='comanda_produtos')
    produto = db.relationship('Product', backref='comanda_produtos')

    def to_dict(self):
        return {
            'id': self.id,
            'comanda_id': self.comanda_id,
            'produto': {
                'id': self.produto.id,
                'name': self.produto.name,  # Correção aqui
                'price': self.produto.price,
                'description': self.produto.description,
            },
            'quantidade': self.quantidade,
            'descricao': self.descricao,
            'preco': self.preco
        }

class ComandaProdutoNaoEncontrado(Exception):
    pass

def adicionar_produto_comanda(comanda_id, produto_id, quantidade, descricao,  preco):
    comanda_produto = ComandaProduto(
        comanda_id=comanda_id,
        produto_id=produto_id,
        quantidade=quantidade,
        descricao=descricao,
        preco=preco
    )
    db.session.add(comanda_produto)
    db.session.commit()
    return comanda_produto.to_dict()

def listar_comanda_produtos():
    comanda_produtos = ComandaProduto.query.all()
    return [cp.to_dict() for cp in comanda_produtos]


def comanda_produto_por_id(id_comanda_produto):
    comanda_produto = ComandaProduto.query.get(id_comanda_produto)  
    if not comanda_produto:
        raise ComandaProdutoNaoEncontrado
    return comanda_produto.to_dict()

def atualizar_pedido(id_comanda_produto, novos_dados):
    comanda_produto = ComandaProduto.query.get(id_comanda_produto)
    if not comanda_produto:
        raise ComandaProdutoNaoEncontrado
    comanda_produto.produto_id = novos_dados.get('produto_id')
    comanda_produto.quantidade = novos_dados.get('quantidade')
    comanda_produto.descricao = novos_dados.get('descricao')
    comanda_produto.preco = novos_dados.get('preco')
    db.session.commit()
    return comanda_produto.to_dict()

def listar_produtos_da_comanda(comanda_id):
    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return []

    pedidos = []
    for pedido in comanda.comanda_produtos:
        pedidos.append({
            "pedido_id": pedido.id,
            "produto_id": pedido.produto.id,
            "nome_produto": pedido.produto.name,
            "quantidade": pedido.quantidade,
            "preco_unitario": pedido.preco,
            "descricao": pedido.descricao
        })
    return pedidos

def calcular_subtotal_comanda(comanda_id):
    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return 0.0

    subtotal = 0.0
    for pedido in comanda.comanda_produtos:
        subtotal += pedido.quantidade * pedido.preco

    return round(subtotal, 2)