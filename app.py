from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

# Directorio donde se guardarán los archivos subidos
UPLOAD_FOLDER = '/opt/sara/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para mostrar el formulario y manejar la carga
@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html', result=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Verificar que se ha subido un archivo
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.rsc'):
        # Guardar el archivo en el servidor
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Ejecutar el script sara.py con el archivo subido como argumento
        result = run_sara(filepath)

        # Eliminar el archivo después de analizarlo
        os.remove(filepath)

        # Mostrar el resultado de la auditoría
        return render_template('upload.html', result=result)

    return "El archivo debe ser un archivo .rsc"

def run_sara(config_file):
    # Ejecutar el script sara.py con el archivo de configuración como argumento
    command = ['python3', '/opt/sara/sara.py', '--config-file', config_file]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout  # Devuelve el resultado de la auditoría

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
