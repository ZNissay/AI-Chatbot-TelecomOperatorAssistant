from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Chat_Inter_optimisé1 import startChat, getquestion, authenticate, create_user, get_user_by_id

app = Flask(__name__)
app.secret_key = 'key'  # Nécessaire pour Flask-Login

# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def home():
       return redirect(url_for('login'))
    
@app.route('/index')
def hello_world():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        user = authenticate(phone_number, password)
        if user:
            login_user(user)
            return redirect(url_for('hello_world'))
        else:
            return jsonify({"message": "Invalid phone number or password"}), 401
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    phone_number = request.form['phone_number']
    password = request.form['password']
    user = authenticate(phone_number, password)
    if user:
        return jsonify({"message": "User already exists"}), 400
    else:
        create_user(phone_number, password)
        return jsonify({"message": "User created successfully"})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": f"Hello, {current_user.phone_number}!"})

@app.route('/predict', methods=['POST'])
def Predict():
    res = getquestion()
    response = jsonify({'result': res})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/chat', methods=['POST'])
@login_required
def Chat():
    data = request.get_json()
    msg = data.get('text', '')
    res = startChat(msg)
    response = jsonify({'result': res, "user": msg})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()
