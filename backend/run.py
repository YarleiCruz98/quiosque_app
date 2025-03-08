from flask import Flask
from app.config import create_app, db
from app.routes.product_routes import product_blueprint

app = create_app()
app.register_blueprint(product_blueprint)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)