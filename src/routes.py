from pathlib import Path
from io import BytesIO
import base64
import requests
from fastai import *
from fastai.vision import *
from PIL import Image as PILImage
import os
import time
import secrets
from flask import render_template, flash, redirect, url_for, session, request
from src.forms import PacienteForm, RespuestaForm, Registration_Form, LogIn_Form
from src import app, tabla_pacientes, bcrypt, tabla_usuarios
from bson.objectid import ObjectId

# Constantes
NAME_OF_FILE = '/app/src/models/covidnocovid_stage-2-resnet34-augmented_tvt' 
PATH_TO_MODELS_DIR = Path('') 
classes = ['covid', 'nocovid']

# Funciones
def setup_model_pth(path_to_pth_file, learner_name_to_load, classes):
    data = ImageDataBunch.single_from_classes(path_to_pth_file, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
    learn = cnn_learner(data, models.resnet34, model_dir='models')
    learn.load(learner_name_to_load, device=torch.device('cpu'))
    return learn
learn = setup_model_pth(PATH_TO_MODELS_DIR, NAME_OF_FILE, classes)
	
def model_predict(img):
    img = open_image(img)
    pred_class,pred_idx,outputs = learn.predict(img)
    formatted_outputs = ["{:.1f}%".format(value) for value in [x * 100 for x in outputs]]
    pred_probs = sorted(
            zip(learn.data.classes, map(str, formatted_outputs)),
            key=lambda p: p[1],
            reverse=True
        )

    result = {"class":pred_class, "probs":pred_probs}
    return result

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn, picture_path

@app.route('/')
def inicio():
    return render_template('index.html', title = 'Inicio')


@app.route('/results/<file_name>', methods = ['GET', 'POST'])
def results(file_name):
    form = RespuestaForm()
    fn = Path('src/static/images', file_name)
    file_path = os.path.join('../static/images', file_name)
    results = model_predict(fn)
    cambios = {
        'diagnostico': str(results['class']),
        'probabilidades': [(results['probs'][0][0], results['probs'][0][1]), (results['probs'][1][0], results['probs'][1][1])]
    }
    tabla_pacientes.update_one({'archivo': file_name}, {'$set': cambios})
    if form.validate_on_submit():
        cambios = {
            'nombre-del-comentario': form.nombre.data,
            'comentario': form.comentarios.data
        }
        tabla_pacientes.update_one({'archivo': file_name},{'$set': cambios})
    return render_template('result.html', title = 'Resultados', file_name = file_path, results= results, form = form, sesion = True)

@app.route('/about')
def about():
    return render_template('about.html', title = 'Sobre Nosotros')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('resultados'))
    login = LogIn_Form()
    if login.validate_on_submit():
        user = tabla_usuarios.find_one({'usuario': login.username.data})
        if user and bcrypt.check_password_hash(user['password'], login.password.data):
            # login_user(user, remember=login.remember.data)
            flash('Inicio de sesión completado satisfactoriamente', 'success')
            session['user'] = user['usuario']
            session['email'] = user['email']
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('resultados'))
        else:
            flash(
                'No se pudo iniciar sesión, por favor revise el usuario y contraseña', 'danger')
    return render_template('inicio_sesion.html', title='Inicio Sesion', form=login)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for('resultados'))
    register = Registration_Form()
    if register.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            register.password.data).decode('utf-8')
        usuario = {'usuario': register.username.data,
                   'password': hashed_pass, 'email': register.email.data, 'image': 'default.jpg', 'colaboradores': ['nada']}
        
        tabla_usuarios.insert_one(usuario)
        session['user'] = register.username.data
        session['email'] = register.email.data
        flash(
            f'Tu cuenta fue creada satisfactoriamente, tu usuario es:{register.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', title='Registro', form=register)


@app.route('/results', methods = ['GET', 'POST'])
def resultados():
    form = PacienteForm()
    if form.validate_on_submit():
        file_name, file_path =save_picture(form.archivo.data)
        paciente = {
            'nombre': form.nombres.data.upper(),
            'apellido': form.apellidos.data.upper(),
            'cedula': form.cedula.data,
            'edad': form.edad.data,
            'sector': form.sector.data,
            'archivo': file_name,
            'path': file_path
        }
        tabla_pacientes.insert_one(paciente)
        return redirect(url_for('results', file_name = file_name))
    return render_template('forms.html', title = 'Covid-19', form = form, sesion = True)    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))
