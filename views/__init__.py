from . import login
from core import app
from flask import redirect

@app.route('/')
def ind():
    return redirect('/login')

from .login import login, logout
app.route('/login', methods=["POST", "GET"])(login)
app.route('/logout', methods=["POST", "GET"])(logout)

from .generar import index, generar_constancias
app.route('/generar')(index)
app.route('/generar_constancias', methods=['POST'])(generar_constancias)


from .catalogos import catalogos, uploadFile
app.route('/catalogos', methods=['POST', 'GET'])(catalogos)
app.route('/uploadfile', methods=['POST'])(uploadFile)