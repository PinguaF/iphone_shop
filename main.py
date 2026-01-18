import json
from flask import Flask, render_template, make_response, request, redirect, flash, url_for, jsonify, abort
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from data.user.User import User
from data.catalog.catalog import get_all_category, Product, get_id_for_product
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

@app.route("/catalog/<category>/<pid>", methods=["POST", "GET"])
def render_product(category, pid):
    #try:
        product = Product(pid, category)
        colors, memorys = product.get_version()
        return render_template(f"product/{category}.html", header=catalog_name[category], 
                               line=product.line, memory=product.memory, 
                               color=product.color, photo=product.photo,
                               category=category, colors=colors, memorys=memorys,
                               price = product.price 
                              )
    #except:
    #   abort(404)

@app.route("/catalog/<category>", methods=["POST", "GET"])
def render_catalog(category):
    try:
        return render_template("catalog_grid.html", 
                               header=catalog_name[category], 
                               products=json.dumps(get_all_category(category)))
    except:
        abort(404)

@app.route("/profile", methods=["POST", "GET"])
def backstore():
    if request.method == "GET":
       pass
    elif request.method == "POST":
        pass

@socketio.on("get_id_by_paramets")
def get_id(data):
    answer = get_id_for_product(data['category'], data['line'], data['color'], data['memory'])
    socketio.emit("id_by_paramets", answer)


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")