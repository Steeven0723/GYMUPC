from flask import Flask, render_template, jsonify, request
from assistant import Imagenes,ICM



import subprocess

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    imagen = Imagenes()
    img_name = imagen.run()
    return render_template('index.html', img_name=img_name)



@app.route('/ejecutar-python')
def ejecutar_python():
    try:
        subprocess.run(["python", "index.py"], check=True, text=True, capture_output=True)
        return jsonify({"success": True, "message": "Script ejecutado correctamente"})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/infGym.html')
def infGym():
    return render_template('infGym.html')

@app.route('/calICM.html')
def calICM():
    imagen = Imagenes()
    img_name = imagen.run()
    return render_template('calICM.html', img_name=img_name)

@app.route('/calcular-imc', methods=['POST'])
def calcular_imc():
    data = request.get_json()
    altura = data['altura']
    peso = data['peso']

    imc = ICM.Calcular(altura, peso)

    # Determinar el estado de peso
    estado_peso = ''
    if imc < 18.5:
        estado_peso = 'Peso insuficiente (IMC inferior a 18.5)'
    elif imc >= 18.5 and imc <= 24.9:
        estado_peso = 'Peso saludable (IMC entre 18.5 y 24.9)'
    elif imc >= 25 and imc <= 29.9:
        estado_peso = 'Sobrepeso (IMC entre 25 y 29.9)'
    else:
        estado_peso = 'Obeso (IMC 30 o más)'

    return jsonify({'imc': imc, 'estadoPeso': estado_peso})


if __name__ == '__main__':
    app.run(debug=True)
