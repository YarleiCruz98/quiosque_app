from flask import request, jsonify, Blueprint
from app.models.order_models import Comanda, ComandaNaoEncontrada, comanda_por_id, listar_comanda, criar_comandas
from app.models.order_product_routes import ComandaProduto, ComandaProdutoNaoEncontrado, atualizar_pedido, listar_produtos_da_comanda, calcular_subtotal_comanda, fechar_comanda, cancelar_comanda
from app.models.product_models import produto_por_id, ProdutoNaoEncontrado, Product, listar_produtos
from app.models.pagamento_models import Pagamento
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
    

@order_blueprint.route('/comandas/<int:comanda_id>/fechar', methods=['POST'])
def fechar_comanda(comanda_id):
    comanda = Comanda.query.get_or_404(comanda_id)
    data = request.get_json()
    print(comanda.status)
    print(data)

    if not data or 'status' not in data:
        return jsonify({'error': 'Campo "status" é obrigatório'}), 400

    if data['status'] != 'fechada':
        return jsonify({'error': 'Valor inválido. O status deve ser "fechada"'}), 400

    if comanda.status == 'fechada':
        return jsonify({'error': 'Comanda já está fechada'}), 400

    comanda.status = 'fechada'
    db.session.commit()
    return jsonify(comanda.to_dict()), 200


@order_blueprint.route('/comandas/<int:comanda_id>/cancelar', methods=['POST'])
def cancelar_comanda(comanda_id):
    comanda = Comanda.query.get_or_404(comanda_id)
    data = request.get_json()

    if not data or 'status' not in data:
        return jsonify({'error': 'Campo "status" é obrigatório'}), 400

    if data['status'] != 'cancelada':
        return jsonify({'error': 'Valor inválido. O status deve ser "cancelada"'}), 400

    if comanda.status == 'cancelada':
        return jsonify({'error': 'Comanda já está cancelada'}), 400

    comanda.status = 'cancelada'
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

    pedidos_formatados = listar_produtos_da_comanda(comanda_id)
    subtotal_original = calcular_subtotal_comanda(comanda_id)
    total_pago = comanda.total_pago or 0
    restante = max(subtotal_original - total_pago, 0)

    resposta = {
        f"comanda-{comanda.id}": {
            "mesa": comanda.mesa,
            "pedidos": pedidos_formatados,
            "subtotal_original": subtotal_original,
            "total_pago": total_pago,
            "faltando_pagar": restante,
            "status": comanda.status,
        }
    }

    return jsonify(resposta), 200


@order_blueprint.route('/comandas/<int:comanda_id>/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(comanda_id, pedido_id):
    pedido = ComandaProduto.query.filter_by(comanda_id=comanda_id, id=pedido_id).first()
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    db.session.delete(pedido)
    db.session.commit()

    return jsonify({'message': 'Pedido deletado com sucesso'}), 200

@order_blueprint.route('/comandas/<int:comanda_id>/pagar', methods=['POST'])
def pagar_comanda(comanda_id):
    comanda = Comanda.query.get(comanda_id)
    if not comanda:
        return jsonify({'error': 'Comanda não encontrada'}), 404

    data = request.get_json()
    valor_pago = data.get('valor_pago')

    if valor_pago is None:
        return jsonify({'error': 'Campo "valor_pago" é obrigatório'}), 400

    try:
        valor_pago = float(valor_pago)
    except ValueError:
        return jsonify({'error': 'Valor inválido para pagamento'}), 400

    subtotal_original = calcular_subtotal_comanda(comanda_id)
    comanda.total_pago = (comanda.total_pago or 0) + valor_pago
    restante = max(subtotal_original - comanda.total_pago, 0)
    troco = 0

    if comanda.total_pago >= subtotal_original:
        comanda.status = 'fechada'
        troco = comanda.total_pago - subtotal_original

    # Salva o pagamento e o troco
    novo_pagamento = Pagamento(
        comanda_id=comanda.id,
        valor_pago=valor_pago,
        troco=troco
    )
    db.session.add(novo_pagamento)
    db.session.commit()

    return jsonify({
        "subtotal_original": subtotal_original,
        "total_pago": comanda.total_pago,
        "faltando_pagar": restante,
        "troco": troco,
        "status": comanda.status
    }), 200