from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para armazenar os dados do usuário e o IMC
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recebe os dados do formulário
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        # Calcula o IMC
        imc = weight / (height ** 2)

        # Cria uma nova entrada no banco de dados
        new_person = Person(name=name, weight=weight, height=height, imc=imc)
        db.session.add(new_person)
        db.session.commit()

        # Redireciona para a página de resultados com o IMC calculado
        return redirect(url_for('result', person_id=new_person.id))

    return render_template('index.html')

@app.route('/result/<int:person_id>')
def result(person_id):
    person = Person.query.get(person_id)
    return render_template('result.html', person=person)

if __name__ == '__main__':
    app.run(debug=True)
