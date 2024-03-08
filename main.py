from flask import Flask, request, jsonify, render_template
from tinydb import TinyDB, Query

app = Flask(__name__)

# Initialize TinyDB
db = TinyDB('caminhos.json')
caminhos = Query()
@app.route('/')
def home():
    return render_template('register.html')
@app.route('/novo',methods=['POST'])
def insertNovo():
    data = request.json
    id = data['id']
    x = data['x']
    y = data['y']
    z = data['z']
    r = data['r']
    if db.search(caminhos.id == id):
        return jsonify({'message': 'o caminho com esse id já existe'}), 409
    db.insert({
        'id': id,
        'x': x,
        'y': y,
        'z': z,
        'r': r
        })
    return jsonify({'message': 'Caminho criado com sucesso'}), 201
@app.route('/pegar_caminho', methods = ['POST'])
def pegarcaminho():
    data = request.json
    id = data['id']
    caminho = db.search(caminhos.id == id)
    if caminho:
        return jsonify(caminho), 200
    return jsonify({'message': 'Caminho não encontrado'}), 404

@app.route('/listas_caminhos',methods = ['GET'])
def listAll():
    return jsonify(db.all())
@app.route('/atualizar',methods = ['POST'])
def update():
    data = request.json
    id = data['id']
    x = data['x']
    y = data['y']
    z = data['z']
    r = data['r']
    if not db.search(caminhos.id == id):
        return jsonify({'message': 'Caminho não encontrado'}), 404
    db.update({'x': x, 'y': y, 'z': z, 'r': r}, caminhos.id == id)
    return jsonify({'message': 'Caminho atualizado com sucesso'}), 200
@app.route('/deletar',methods = ['POST'])
def delete():
    data = request.json
    id = data['id']
    if not db.search(caminhos.id == id):
        return jsonify({'message': 'Caminho não encontrado'}), 404
    db.remove(caminhos.id == id)
    return jsonify({'message': 'Caminho deletado com sucesso'}), 200
if __name__ == '__main__':
    app.run(host='localhost',port=3000,debug=False)
