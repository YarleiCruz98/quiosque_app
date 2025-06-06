# from flask import Flask
# from app.config import create_app, db
# from app.routes.product_routes import product_blueprint
# from app.routes.order_routes import order_blueprint
# from flask_cors import CORS

# app = create_app()

# CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
# app.register_blueprint(product_blueprint)
# app.register_blueprint(order_blueprint)
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(host="0.0.0.0", port=5000, debug=True)

# main.py
from app.config import create_app, db
from app.routes.product_routes import product_blueprint
from app.routes.order_routes import order_blueprint

app = create_app()  # Aqui o app já está com CORS

app.register_blueprint(product_blueprint)
app.register_blueprint(order_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
