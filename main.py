import json
from flask import Flask, render_template, make_response, request, redirect, flash, url_for, jsonify, abort
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from data.user.User import User, register_new_user, get_id_from_email
from data.catalog.catalog import get_all_category, Product, get_id_for_product, transform_order
from config.names import catalog_name


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)



@app.route("/", methods=["POST", "GET"])
def main():
    return render_template("main.html")

@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return render_template("auth/profile.html", first_name=current_user.first_name, last_name=current_user.last_name,
                           email=current_user.email, id=current_user.id, phone=current_user.phone, address=current_user.address)

@app.route("/orders", methods=["POST", "GET"])
@login_required
def orders():
    return render_template("auth/orders.html", first_name=current_user.first_name, last_name=current_user.last_name,
                           email=current_user.email, id=current_user.id)

@app.route("/register", methods=["POST"])
def register_post():
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    repassword = request.form.get("repassword")
    if password == repassword:
        if register_new_user(first_name, last_name, email, password):
            id = get_id_from_email(email)
            user = User(id)
            login_user(user)
            return redirect('/profile')
        else:
            return redirect('/login?error=alreadyindb')
    else:
        return redirect('/register?error=passwordisincorrect')


@app.route("/register", methods=["GET"])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template("auth/register.html")
    

@app.route("/login", methods=["POST"])
def login_post():
    try:
        email = request.form.get("email")
        id = get_id_from_email(email)
        password = request.form.get("password")
        user = User(id)
        if user.check_password(password):
            login_user(user)
            return redirect('/profile')
        else:
            return redirect('/login?error=dataisincorrect')
    except:
        print('=====================Произошла ошибка')
        return redirect('/login?error=dataisincorrect')


@app.route("/login", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template("auth/login.html")
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect('/')


@app.route("/cart", methods=["POST", "GET"])
@login_required
def cart():
    cart, end_price = transform_order(current_user.cart)
    return render_template("cart.html", cart=cart, end_price=end_price)

@app.errorhandler(401)
def error_handler(error):
    return redirect(url_for('login_get'))

@app.route("/catalog/<category>/<pid>", methods=["POST", "GET"])
def render_product(category, pid):
    #try:
        product = Product(pid, category)
        colors, memorys = product.get_version()
        return render_template(f"product/{category}.html", header=catalog_name[category], 
                               line=product.line, memory=product.memory, 
                               color=product.color, photo=product.photo,
                               category=category, colors=colors, memorys=memorys,
                               price=product.price, id=product.id
                              )
    #except:
    #   abort(404)

@app.route("/catalog/<category>", methods=["POST", "GET"])
def render_catalog(category):
    #try:
        return render_template("catalog_grid.html", products=json.dumps(get_all_category(category)),
                               header=catalog_name[category])
    #except:
        #abort(404)


@socketio.on('connect')
def handle_connect():
    room = request.sid
    join_room(room)
    send(f'Вы присоеденились к комнате {room}', to=room)


@socketio.on("get_id_by_paramets")
def get_id(data):
    room = request.sid
    answer = get_id_for_product(data['category'], data['line'], data['color'], data['memory'])
    socketio.emit("id_by_paramets", answer, to=room)

@socketio.on("add_to_cart")
def get_id(data):
    room = request.sid
    if current_user.is_authenticated:
        product = Product(data['id'], data['category'])
        if not current_user.cart:
            cart = {
                f'{product.category}': {
                    f'{product.id}': {
                        'count': 1
                    }
                }
            }
        elif product.id in current_user.cart[product.category].keys():
            cart = current_user.cart
            cart[product.category][product.id]['count'] += 1
            if cart[product.category][product.id]['count'] > 10: cart[product.category][product.id]['count'] = 10
        else:
            cart = current_user.cart
            cart[product.category][product.id] = { 'count': 1 }
        current_user.set_cart(cart)
        print(cart)
        emit("answer_cart", {'answer':'400'}, to=room)
    else:
        emit("answer_cart", {'answer':'401'}, to=room)#error not auth

@socketio.on("minus_from_cart")
def get_id(data):
    room = request.sid
    if current_user.is_authenticated:
        product = Product(data['id'], data['category'])
        if not current_user.cart:
            emit("answer_cart", {'answer':'405'}, to=room)
        else:
            cart = current_user.cart
            cart[product.category][product.id]['count'] -= 1
            if cart[product.category][product.id]['count'] == 0: 
                cart[product.category].pop(product.id)
            if not cart[product.category]:
                cart.pop(product.category)
        current_user.set_cart(cart)
        print(cart)
        emit("answer_cart", {'answer':'400'}, to=room)
    else:
        emit("answer_cart", {'answer':'401'}, to=room)#error not auth

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")