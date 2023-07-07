from flask import Flask
from app.azureai.auzre_ai import azure_ai

app = Flask(__name__)

app.register_blueprint(azure_ai, url_prefix='/azure')


@app.route('/')
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
