from flask import request, jsonify, Blueprint
from app.models.order_models import Comanda, Pedido, ComandaNaoEncontrada, comanda_por_id, listar_comanda
from app.models.order_product_routes import ComandaProduto, ComandaProdutoNaoEncontrado, atualizar_pedido
from app.models.product_models import produto_por_id, ProdutoNaoEncontrado, Product
from app.config import db

order_blueprint = Blueprint('order_bp', __name__)
#Rotas para Comanda

@order_blueprint.route('/comandas', methods=['POST'])
def criar_comanda():
    data = request.get_json()
    mesa = data.get('mesa')
    data_abertura = data.get('data_abertura')

    if not mesa:
        return jsonify({'error' : 'Número da mesa é obrigatório'}), 400
    
    #Adiciona nova comanda no banco de dados
    nova_comanda = Comanda.criar_comanda(mesa, data_abertura)
    db.session.add(nova_comanda)
    db.session.commit()

    return jsonify(nova_comanda.to_dict()) , 201

@order_blueprint.route('/comandas', methods=['GET'])
def listar_comanda():
    comanda = listar_comanda()
    return jsonify(comanda), 200

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
    
    comanda = get_comandaPorId(comanda_id)
    if not comanda:
        return jsonify({'error': 'Comanda não encontrada'}), 404
    
    try:
        produto = produto_por_id(produto_id)
    except ProdutoNaoEncontrado:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    novo_pedido = ComandaProduto(comanda_id=comanda_id, produto_id=produto_id, quantidade=quantidade, preco=produto.preco, descricao=descricao)
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify(novo_pedido.to_dict()), 201

# alterar pedido
@order_blueprint.route('/comandas/<int:comanda_id>/pedidos/<int:pedido_id>', methods=['PUT'])
def atualizar_pedido(comanda_id, pedido_id):
    data = request.get_json()
    
    pedido = Pedido.query.filter_by(comanda_id=comanda_id, id=pedido_id).first()
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    atualizar_pedido(comanda_id,data)
    
    return jsonify(pedido.to_dict()), 200


@order_blueprint.route('/comanda/<int:comanda_id>/pedidos', methods=['GET'])
def listar_pedidos(comanda_id):
    # Verificar se a comanda existe
    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return jsonify({'error': 'Comanda não encontrada'}), 404

    # Buscar os produtos associados à comanda
    comanda_produtos = ComandaProduto.query.filter_by(comanda_id=comanda_id).all()

    # Se não houver pedidos
    if not comanda_produtos:
        return jsonify({'message': 'Nenhum pedido associado a esta comanda'}), 200

    # Preparar a resposta em formato de dicionário
    pedidos = []
    valor_total_comanda = 0.0  # Variável para armazenar o valor total da comanda

    for item in comanda_produtos:
        produto = Product.query.get(item.produto_id)
        
        # Calcular o valor total do item (preço unitário * quantidade)
        valor_total_item = produto.preco * item.quantidade
        
        # Atualizar o valor total da comanda
        valor_total_comanda += valor_total_item

        pedidos.append({
            'produto': produto.nome,
            'quantidade': item.quantidade,
            'valor_unitario': produto.preco,
            'valor_total_item': valor_total_item
        })

    # Retornar a lista de pedidos com o valor total da comanda
    return jsonify({
        'comanda_id': comanda_id,
        'pedidos': pedidos,
        'valor_total_comanda': valor_total_comanda
    })