from flask import request, jsonify, Blueprint
from app.models.order_models import Comanda, ComandaNaoEncontrada, comanda_por_id, listar_comanda, criar_comandas
from app.models.order_product_routes import ComandaProduto, ComandaProdutoNaoEncontrado, atualizar_pedido, listar_produtos_da_comanda, calcular_subtotal_comanda
from app.models.product_models import produto_por_id, ProdutoNaoEncontrado, Product, listar_produtos
from app.config import db

order_blueprint = Blueprint('order_bp', __name__)
#Rotas para Comanda

@order_blueprint.route('/comandas/criar', methods=['POST', 'GET'])
def criar_comanda():
    try:
        data = request.get_json()
        mesa = data.get('mesa')
        data_abertura = data.get('data_abertura')

        if not mesa:
            return jsonify({'error': 'Número da mesa é obrigatório'}), 400

        nova_comanda = criar_comandas(mesa, data_abertura)

        return jsonify(nova_comanda), 201  # Retorna o objeto convertido para JSON

    except Exception as e:
        return jsonify({'error': f'Erro ao criar comanda: {str(e)}'}), 500


@order_blueprint.route('/comandas', methods=['GET'])
def listar_comanda_route():
    comandas = listar_comanda()  # chama a função correta
    return jsonify(comandas)

@order_blueprint.route("/comandas/<int:id_order>", methods=["GET"])
def get_comandaPorId(id_order):
    try:
        comanda = comanda_por_id(id_order)
        return jsonify(comanda), 200
    except ComandaNaoEncontrada:
        return jsonify({"erro": 'Comanda nao encontrada'}), 404
    

@order_blueprint.route('/comandas/<int:comanda_id>/fechar', methods=['PUT'])
def fechar_comanda(order_id):
    comanda = Comanda.query.get_or_404(order_id)
    
    if comanda.status == 'fechada':
        return jsonify({'error': 'Comanda já está fechada'}), 400
    
    comanda.status = 'fechada'
    db.session.commit()
    
    return jsonify(comanda.to_dict()), 200    
    
@order_blueprint.route('/comandas/<int:comanda_id>/pedidos', methods=['POST']) 
def adicionar_pedido(comanda_id):
    data = request.get_json()
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade', 1)
    descricao = data.get('descricao')

    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return jsonify({'error': 'Comanda não encontrada'}), 404

    try:
        produto = Product.query.get(produto_id)
        if not produto:
            raise ProdutoNaoEncontrado
    except ProdutoNaoEncontrado:
        return jsonify({'error': 'Produto não encontrado'}), 404

    novo_pedido = ComandaProduto(
        comanda_id=comanda_id,
        produto_id=produto_id,
        quantidade=quantidade,
        preco=produto.price,
        descricao=descricao
    )
    db.session.add(novo_pedido)
    db.session.commit()

    # Buscar todos os pedidos atuais da comanda após adicionar
    pedidos_formatados = listar_produtos_da_comanda(comanda_id)
    subtotal = calcular_subtotal_comanda(comanda_id)
    resposta = {
        f"comanda-{comanda.id}": {
            "mesa": comanda.mesa,
            "pedidos": pedidos_formatados,
            "subtotal": subtotal,
            "status": comanda.status,
        }
    }

    return jsonify(resposta), 201


# alterar pedido
@order_blueprint.route('/comandas/<int:comanda_id>/pedidos/<int:pedido_id>', methods=['PUT'])
def atualizar_pedido(comanda_id, pedido_id):
    data = request.get_json()

    pedido = ComandaProduto.query.filter_by(comanda_id=comanda_id, id=pedido_id).first()
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    # Atualiza os campos permitidos
    if 'quantidade' in data:
        pedido.quantidade = data['quantidade']
    if 'descricao' in data:
        pedido.descricao = data['descricao']
    
    db.session.commit()

    return jsonify({
        'id': pedido.id,
        'produto': pedido.produto.name,
        'quantidade': pedido.quantidade,
        'preco_unitario': pedido.preco,
        'descricao': pedido.descricao
    }), 200



@order_blueprint.route('/comandas/<int:comanda_id>/pedidos', methods=['GET'])
def listar_pedidos(comanda_id):
    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return jsonify({'error': 'Comanda não encontrada'}), 404

    comanda_produtos = ComandaProduto.query.filter_by(comanda_id=comanda_id).all()
    if not comanda_produtos:
        return jsonify({'message': 'Nenhum pedido associado a esta comanda'}), 200
    
    pedidos_formatados = listar_produtos_da_comanda(comanda_id)
    subtotal = calcular_subtotal_comanda(comanda_id)
    resposta = {
        f"comanda-{comanda.id}": {
            "mesa": comanda.mesa,
            "pedidos": pedidos_formatados,
            "subtotal": subtotal,
            "status": comanda.status,
        }
    }

    return jsonify(resposta), 201