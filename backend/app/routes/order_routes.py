from flask import request, jsonify, Blueprint
from app.models.order_models import Comanda, Pedido
from app.models.product_models import produto_por_id, ProdutoNaoEncontrado
from app.config import db

order_blueprint = Blueprint('order_bp', __name__)
#Rotas para Comanda

@order_blueprint.route('/comandas', methods=['POST'])
def criar_comanda():
    data = request.get_json()
    mesa = data.get('mesa')

    if not mesa:
        return jsonify({'error' : 'Número da mesa é obrigatório'}), 400
    
    #Adiciona nova comanda no banco de dados
    nova_comanda = Comanda(mesa=mesa)
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
    


    




    


