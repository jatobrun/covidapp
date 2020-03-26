from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from src import tabla_usuarios
from flask import session

class PacienteForm(FlaskForm):
    nombres = StringField('Nombre del paciente:', validators=[DataRequired()])
    apellidos = StringField('Apellidos del paciente:', validators=[DataRequired()])
    cedula = IntegerField('Cédula de Ciudadanía: ', validators = [DataRequired()])
    edad = IntegerField('Edad:', validators =[DataRequired()])
    sector = SelectField('¿A qué zona pertenece?', choices=[('9  DE OCTUBRE', '9 DE OCTUBRE'), ('ALBORADA', 'ALBORADA'), ('ATARAZANA', 'ATARAZANA'), ('BASTION POPULAR', 'BASTION POPULAR'), ('BELLAVISTA', 'BELLAVISTA'), ('CEIBOS', 'CEIBOS'), ('CENTENARIO', 'CENTENARIO'), ('CHONGON', 'CHONGON'), ('CRISTO DEL CONSUELO', 'CRISTO DEL CONSUELO'), ('ESTEROS', 'ESTEROS'), ('FLOR DE BASTION', 'FLOR DE BASTION'), ('FLORESTA', 'FLORESTA'), ('FLORIDA', 'FLORIDA'), ('FORTIN', 'FORTIN'), ('GUASMO', 'GUASMO'), ('GUAYACANES', 'GUAYACANES'), ('ISLA TRINITARIA', 'ISLA TRINITARIA'), ('KENNEDY', 'KENNEDY'), ('MAPASINGUE', 'MAPASINGUE'), ('MARTHA DE ROLDOS', 'MARTHA DE ROLDOS'), ('MONTE SINAI', 'MONTE SINAI'), ('MUCHO LOTE', 'MUCHO LOTE'), ('ORQUIDEAS', 'ORQUIDEAS'), ('PASCUALES', 'PASCUALES'), ('PORTETE', 'PORTETE'), ('PUNTILLA', 'PUNTILLA'), ('SAMANES', 'SAMANES'), ('SAMBORONDON', 'SAMBORONDON'), ('SAUCES', 'SAUCES'), ('SUBURBIO', 'SUBURBIO'), ('URDESA', 'URDESA')])
    archivo = FileField('Cargar radiografia:', validators=[FileAllowed(['jpg', 'jpeg', 'tif', 'png'])])
    submit = SubmitField('Enviar')

class RespuestaForm(FlaskForm):
    nombre = StringField('Nombre:', validators=[DataRequired()])
    comentarios = TextAreaField('Comentario:', validators=[DataRequired()])
    submit = SubmitField('Enviar comentario')


class Registration_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(message = 'Ingrese un usuario porfavor'), Length(min=6, max=20, message='El usuario debe tener mínimo 6 caracteres')])
    email = StringField('Email', validators=[DataRequired(message='Ingrese un email porfavor'), Email(message='No es un correo válido ')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Ingrese una contraseña porfavor')])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
                                     DataRequired(message = 'Confirme su contraseña porfavor'), EqualTo('password', message = 'Las contraseñas ingresadas no son las mismas')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = tabla_usuarios.find_one({'usuario': username.data})
        if user:
            raise ValidationError(
                'Este usuario no está disponible. Por favor ingrese otro.')

    def validate_email(self, email):
        email = tabla_usuarios.find_one({'email': email.data})
        if email:
            raise ValidationError(
                'Este email ya está registrado. Por favor inicie sesión o recupere su contraseña')
 

class LogIn_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField(' Recordar mi usuario')
    submit = SubmitField('Iniciar Sesión')