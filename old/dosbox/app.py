from flask import Flask, request, jsonify
from lib.database import Database  # Importa tu clase que controla DOSBox
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#Buscar un porgrama
@app.route('/specfic-program-data', methods=['POST'])
def get_specific_program_data():
    data = request.get_json()
    program_name = data.get('program_name')  # Nombre del programa que quieres buscar
    db = Database()  # Instancia de tu clase que controla DOSBox
    
    try:
        result = db.get_specific_program_data(program_name)  # Ejecuta y procesa en DOSBox
        return jsonify(result=result), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# Ruta para devolver todos los programas registrados
@app.route('/get-all-programs', methods=['GET'])
def get_all_programs():
    db = Database()
    
    try:
        programs = db.get_programs()  # Obtiene la lista de programas
        return jsonify(programs=programs), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/tape', methods=['POST'])
def get_all_programs_by_tape():
    db = Database()
    data = request.get_json()
    tape_name = data.get('tape_name')
    
    try:
        programs = db.get_programs_by_tape(tape_name)  # Obtiene la lista de programas
        return jsonify(programs=programs), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



# Ruta para obtener la cuenta total de registros
@app.route('/total-reg-count', methods=['GET'])
def total_reg_count():
    db = Database()
    
    try:
        count = db.get_total_reg_count()  # Obtiene el conteo total de registros
        return jsonify(total_register_count=count), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    # Flask estará configurado para escuchar en cualquier IP
    app.run(host='0.0.0.0', port=5000)
