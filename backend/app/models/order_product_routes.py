from app.config import db

class ComandaProduto(db.Model):
    __tablename__ = 'comanda_produtos'    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id', ondelete='CASCADE'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    descricao = db.Column(db.String(255), nullable=True)  # Campo opcional para descrição do produto
    # Definindo o relacionamento para facilitar o acesso às informações de Comanda e Produto
    preco = db.Column(db.Float, nullable=False)  # Preço do produto na comanda
    comanda = db.relationship('Comanda', backref=db.backref('comanda_produtos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('comanda_produtos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'comanda': self.comanda,
            'produto': self.produto,
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