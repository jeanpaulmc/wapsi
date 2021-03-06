from distutils import core
from enum import unique
from operator import sub
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from sqlalchemy import sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Softjuandius_25@localhost:5432/wapsi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# AQUI VAN LAS ENTIDADES


class Usuario(db.Model):
    __tablename__ = 'usuario'
    fecha_nacimiento = db.Column(db.String(50), nullable=False)
    billetera = db.Column(db.Integer, default=0)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), primary_key = True) 
    contrasenia = db.Column(db.String(50), nullable=False)
    barra = db.Column(db.Integer, default=0)


class Tarjeta(db.Model):
    __tablename__ = 'tarjeta'
    codigo = db.Column(db.Integer, primary_key=True)
    codigo_usuario = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)


class Compra(db.Model):
    __tablename__ = 'compra'
    codigo = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.Date, nullable=False)
    precio = db.Column(db.Integer, nullable=False)


class Llamacoin(db.Model):
    __tablename__ = 'llamacoin'
    codigo = db.Column(db.Integer, primary_key=True)
    paquete = db.Column(db.String(20), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    compra_codigo = db.Column(db.Integer, db.ForeignKey(
        'compra.codigo'), nullable=False)
    usuario_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)


class Buyers(db.Model):
    __tablename__ = 'buyers'
    codigo = db.Column(db.Integer, primary_key=True)
    buyer_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)


class Desarrollador(db.Model):
    __tablename__ = 'desarrollador'
    codigo = db.Column(db.Integer, primary_key=True)
    desarrollador_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)


class Compra_producto(db.Model):
    __tablename__ = 'compra_producto'
    codigo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    usuario_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)
    compra_codigo = db.Column(db.Integer, db.ForeignKey(
        'compra.codigo'), nullable=False)


class Producto(db.Model):
    __tablename__ = 'producto'
    codigo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    desarrollador_codigo = db.Column(db.Integer, db.ForeignKey(
        'desarrollador.codigo'), nullable=False)


class Ruleta(db.Model):
    __tablename__ = 'ruleta'
    codigo = db.Column(db.Integer, primary_key=True)
    descuento = db.Column(db.Integer, default=0)
    resultado = db.Column(db.String(50), nullable=False)
    usuario_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)


class Tiempo_juega(db.Model):
    __tablename__ = 'tiempo_juega'
    producto_codigo = db.Column(db.Integer, db.ForeignKey(
        'producto.codigo'), nullable=False)
    usuario_codigo = db.Column(db.String(50), db.ForeignKey(
        'usuario.correo'), nullable=False)
    codigo = db.Column(db.Integer, primary_key=True)
    nro_horas = db.Column(db.Integer, default=0)


db.create_all()

# REGISTRAR USUARIOS


@app.route('/users/create', methods=['POST'])
def create_user():
    error = False
    response = {}
    try:
        fecha_nacimiento = request.get_json()['fecha_nacimiento']
        nombre = request.get_json()['nombre']
        apellido = request.get_json()['apellido']
        correo = request.get_json()['correo']
        contrasenia = request.get_json()['contrasenia']
        option = request.get_json()['tipo']
        user = Usuario(fecha_nacimiento=fecha_nacimiento, nombre=nombre,
                       apellido=apellido, correo=correo, contrasenia=contrasenia)
        db.session.add(user)
        db.session.commit() # TIENE QUE EXISTIR PRIMERO EL USUARIO PARA QUE EXISTA EL DESARROLLADOR
        if option == "Desarrollador":
            des = Desarrollador(desarrollador_codigo = correo)
            db.session.add(des)
            db.session.commit()
        else:
            buyer = Buyers(buyer_codigo = correo)
            db.session.add(buyer)
            db.session.commit()
        response['correo'] = user.correo
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = "[BE] - something went wrong"
    response['error'] = error
    return jsonify(response)

# LOGEAR USUARIOS

@app.route('/authenticate/login', methods=['POST'])
def authenticate_user():
    error = False
    response = {}
    try:
        correo = request.get_json()['correo']
        contrasenia = request.get_json()['password']
        user = db.session.query(Usuario).filter(Usuario.correo == correo).filter(
            Usuario.contrasenia == contrasenia).one()
        response['correo'] = user.correo
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = "Usuario o contrase??a incorrecto"
    response['error'] = error
    return jsonify(response)

# POSTEAR PRODUCTOS

@app.route('/publish/product', methods=['POST'])
def publish_product():
    error = False
    response = {}
    try:
        name = request.get_json()['name']
        price = request.get_json()['price']
        features = request.get_json()['categoria']
        correo = request.get_json()['correo']

        data=Desarrollador.query.filter_by(desarrollador_codigo=correo).first()

        producto = Producto(nombre=name,precio=int(price),categoria=features,desarrollador_codigo = data.codigo)
        db.session.add(producto)
        db.session.commit()
        response['correo'] = correo

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = 'No se pudo ingresar a la base de datos'
    response['error'] = error
    return jsonify(response)

# DELETE PRODUCTOS

@app.route('/product/<product_id>/delete-product', methods=['DELETE'])
def delete_producto_by_id(product_id):
    response = {}
    error = False
    try:
        producto = db.session.query(Producto).filter(
            Producto.codigo == product_id).first()
        if producto is None:
            response['error_message'] = 'product_id does not exists in the database'
        db.session.delete(producto)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    response['success'] = error
    return jsonify(response)

# RECARGAR SALDO
'''
@app.route('/recharge/wallet', methods=['PUT'])
def recharge_wallet():
    response = {}
    error = False
    try:
        dni = request.get_json()['DNI']
        price = request.get_json()['price']
        user = db.session.query(Usuario).filter(Usuario.dni == dni).first()
        user.dinero = user.dinero + float(price)
        response['error_message'] = 'RECARGA EXITOSA'
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = 'No se pudo ingresar a la base de datos'
    response['error'] = error
    return jsonify(response)

#EDITAR UN PRODUCTO
@app.route('/product/<product_id>/edit-product', methods=['PUT'])
def edit_product_by_id(product_id):
    response = {}
    error = False
    try:
        id = Producto.query.get(product_id)
        user = db.session.query(Producto).filter(Producto.id==id).first()
        db.session.execute(sql,(user.name,user.price,user.features))
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    response['error'] = error
    return jsonify(response)
    
'''


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/homepage/<correo>')
def homepage(correo):
    print("Hola")
    data=Desarrollador.query.filter_by(desarrollador_codigo=correo).first()
    my_products = db.session.query(Producto).filter(Producto.desarrollador_codigo==data.codigo)
    return render_template('homepage.html',data=Usuario.query.filter_by(correo=correo).first(), data2=my_products)

@app.route('/products/<correo>')
def products(correo):
    return render_template('products.html', data=Desarrollador.query.filter_by(desarrollador_codigo=correo).first())

@app.route('/recharge/<correo>')
def recharge(correo):
    return render_template('recharge.html', data=Usuario.query.filter_by(correo=correo).first())

@app.route('/tarjet/')
def tarjet():
    return render_template('tarjet.html')

if __name__ == '__main__':
    app.run(port=5003, debug=True)
else:
    print('using global variables from FLASK')
