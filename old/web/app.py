from flask import Flask, render_template, request, redirect, session
from lib.database import Database

app = Flask(__name__)


YES = "Y"
NO = "N"


@app.route('/', methods=['GET'])
def index():
    db = Database()
    data = {
        "numReg": db.get_total_reg_count(),
        "found": YES,
        "data": db.get_programs()
    }
    return render_template('index.html', data=data)

@app.route('/name',methods=['POST'])
def name_post():
    db = Database()
    program_name = request.form['name'].upper()
    program = db.get_specific_program_data(program_name)
    
    data = {
        "numReg": db.get_total_reg_count(),
        "found": NO,
        "data": []
    }
    if len(program) > 0:
        data["found"] = YES
        data["data"] = program
    return render_template("index.html",data=data)

@app.route('/tape', methods=['POST'])
def cinta_post():
    db = Database()
    try:
        tape_name = request.form['tape'].upper()
        programs_in_tape = db.get_programs_by_tape(tape_name)
        data = {
            "numReg": db.get_total_reg_count(),
            "found": NO,
            "data": []
        }
        if len(programs_in_tape) > 0:
            data["found"] = YES
            data["data"] = programs_in_tape
    except Exception as e:
        print(f"Error en cinta_post: {e}")
        return "Error en el servidor", 500

    return render_template("index.html", data=data)



if __name__ == '__main__':
    db = Database()
    app.run(host='0.0.0.0',port=8080)