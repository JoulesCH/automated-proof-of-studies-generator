from flask import render_template, request, redirect
from data import getDbData, saveData
import requests
import base64

from secret import login_required

apikey = 'c65103256fa8bab3d91fd5d74a702f84'

data = getDbData()

@login_required
def catalogos():
    if request.method == "GET":
        data = getDbData()
        return render_template(
            'catalogos.html',
            data=data
            )

    data = request.form
    data = saveData(data)
    return render_template(
            'catalogos.html',
            data=data, 
            cambios=True
            )

def uploadFile():
    if request.method == "POST":
        file = request.files['file']
        # Transform the file to base 64 bytes string 
        params = dict(
            key=apikey,
            image=base64.b64encode(file.read()),
            expiration=604800,
        )

        response = requests.post('https://api.imgbb.com/1/upload', data=params)

        if response.status_code == 200:
            return {
                'image_url': response.json()['data']['url']
                }
        else:
            return {'error': 'Error al subir la imagen'}, 500


