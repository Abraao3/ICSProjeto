from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO (TABELA)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Criar banco
with app.app_context():
    db.create_all()

# 🔹 READ + CREATE
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        usuario = Usuario(nome=nome, email=email)
        db.session.add(usuario)
        db.session.commit()

        return redirect('/')

    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

# 🔹 DELETE
@app.route('/deletar/<int:id>')
def deletar(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/')

# 🔹 UPDATE (carrega página de edição)
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']

        db.session.commit()
        return redirect('/')

    return render_template('editar.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
