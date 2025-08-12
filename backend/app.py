from flask import Flask
from flask_cors import CORS
from models import db
from cron.cron_crawler import start_crawler
from views.usuario_views import rotas_usuario
from views.crawler_views import rotas_cron
from views.assinatura_views import rotas_assinatura

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/redot'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    db.init_app(app)

    rotas_usuario(app)
    rotas_cron(app)
    rotas_assinatura(app)

    start_crawler(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)