from flask import request, jsonify, Blueprint
from app.models.product_models import Product, produto_por_id, ProdutoNaoEncontrado, atualizar_produto, deletar_produto_por_id, listar_produtos
from app.config import db

product_blueprint = Blueprint('product_bp', __name__)

@product_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bem-vindo Ao quiosque Areia Sereia!'}), 200

@product_blueprint.route('/products/', methods=['POST'])
def create_product():
    data = request.get_json()
    # Obtém os dados do formulário
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    description = data.get('description')  # Campo opcional

    # Validação dos campos obrigatórios
    if not name or not price or not stock:
        return jsonify({'error': 'Campos obrigatórios faltando: name, price, stock'}), 400

    # Converte price e stock para os tipos corretos
    try:
        price = float(price)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({'error': 'Preço e estoque devem ser números válidos'}), 400

    # Cria um novo produto com os dados recebidos
    new_product = Product(
        name=name,
        price=price,
        stock=stock,
        description=description
    )

    # Adiciona o novo produto ao banco de dados
    db.session.add(new_product)
    db.session.commit()

    # Retorna o produto criado em formato JSON com status 201 (Created)
    return jsonify(new_product.to_dict()), 201


@product_blueprint.route('/products', methods=['GET'])
def get_product():
    produtos = listar_produtos()
    return jsonify(produtos), 200 

@product_blueprint.route("/products/<int:id_product>", methods=["GET"])
def get_produtoPorId(id_product):
    try:
        produto = produto_por_id(id_product)
        return jsonify(produto), 200
    except ProdutoNaoEncontrado:
        return jsonify({"erro": 'Produto nao encontrado'}), 404
    
@product_blueprint.route("/products/<int:id_product>/atualizar", methods=["PUT", "POST", "GET"])
def update_product(id_product):
    data = request.get_json()
    try:  
        produto = produto_por_id(id_product)
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        description = data.get('description')
        produto['name'] = name
        produto['price'] = price
        produto['stock'] = stock
        produto['description'] = description
        atualizar_produto(id_product, produto)
        print(produto)
        return jsonify(produto), 201
    except ProdutoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@product_blueprint.route("/products/<int:id_product>/delete", methods=["DELETE"])
def delete_product(id_product):
    try:
        produto = produto_por_id(id_product)
        deletar_produto_por_id(id_product)
        return jsonify(f"produto deletado: id {id_product}"), 200
    except ProdutoNaoEncontrado:
        return jsonify({'message': 'Produto não encontrado'}), 404
