from app.config import db

class Product(db.Model):

    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'description': self.description
        }
class ProdutoNaoEncontrado(Exception):
     pass

def listar_produtos():
    products = Product.query.all()
    return [p.to_dict() for p in products]

def produto_por_id(id_product):
    product = Product.query.get(id_product)
    if not product:
        raise ProdutoNaoEncontrado
    return product

def atualizar_produto(id_product, novos_dados):
    produto = Product.query.get(id_product)
    if not produto:
        raise ProdutoNaoEncontrado
    produto.name = novos_dados.get('name')
    produto.price = novos_dados.get('price')
    produto.stock = novos_dados.get('stock')
    produto.description = novos_dados.get('description')
    db.session.commit()
    return produto.to_dict()

def deletar_produto_por_id(id_product):
     produto = Product.query.get(id_product)
     if not produto:
         raise ProdutoNaoEncontrado
     db.session.delete(produto)
     db.session.commit()
