from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/protocolo')
def protocolo():
    return render_template('protocolo.html')

@app.route('/exame')
def exame():
    return render_template('exame.html')

@app.route('/salvar_protocolo', methods=['GET','POST'])
def salvar_protocolo():
    if request.method == 'POST':
        protocol = request.form['protocol'] 
        Intensity_Red = request.form['Intensity_Red']
        Intensity_Green = request.form['Intensity_Green']
        Intensity_Blue = request.form['Intensity_Blue']
        Intensity_White = request.form['Intensity_White']

        new_path = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\protocolo.txt'      

        print (new_path)
        arquivo = open(new_path, 'w')
        arquivo.write("protocol:"+protocol+"\n")
        arquivo.write("Intensity_Red:"+Intensity_Red+"\n")
        arquivo.write("Intensity_Green:"+Intensity_Green+"\n")
        arquivo.write("Intensity_Blue:"+Intensity_Blue+"\n")
        arquivo.write("Intensity_White:"+Intensity_White+"\n")
        arquivo.close()
        print (protocol+"\n")
        print (Intensity_Red+"\n")
        print (Intensity_Green+"\n")
        print (Intensity_Blue+"\n")
        print (Intensity_White+"\n")
    return redirect("/")

@app.route('/executar_exame', methods=['GET','POST'])
def executar_exame():
    if request.method == 'POST':
        estimulo = request.form['estimulo'] 
        gravar = request.form['gravar']

        new_path = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\exame.txt'      

        print (new_path)
        arquivo = open(new_path, 'w')
        arquivo.write(estimulo+";"+gravar)
        print (protocolo)
    return redirect("/")




if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')