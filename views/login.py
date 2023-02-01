from flask import render_template, request, redirect, make_response 
from secret import user_name, password_name, login_required, not_login_required, set_login_cookies, delete_login_cookies


@not_login_required
def login(): 
    if request.method == 'GET':  
        return render_template('login.html')
    
    # Si es un POST
    data = request.form
        
    # validar datos
    if data['username']==user_name and data['password']==password_name:
        next_ = request.args.get('next')
        if str(next_) != 'None':
            ruta = next_
        else:
            ruta = '/generar'
        m_response = set_login_cookies(ruta)
    else:
        m_response = make_response(render_template('login.html', error='Usuario o contraseña inválidas'))

    return m_response

@login_required
def logout():
    response = delete_login_cookies(make_response(redirect('/login')))
    return response