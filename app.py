from api import Tokens
from flask import Flask , send_file , render_template
from flask_restful import Api
import os
app = Flask("Quintex")
api = Api(app)
port = os.environ.get('PORT')
__version__ = '1.0.1'
api.add_resource(Tokens , '/tokens')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files/<filename>')
def logger(filename):
    try:
        # file = open(f'files/{filename}' , 'r')
        return send_file(f'files/{filename}' )
    except FileNotFoundError:
        return """
        <div style="text-align: center;font-family: Arial;font-weight: bold;font-size: 48px;">
            Not Found
        </div>
                <div style="text-align: center;font-family: Arial;font-weight: regular;font-size: 32px;">
            This file doesn't exist on the server
        </div>
                        <div style="text-align: center;font-family: Arial;font-style: italic;font-size: 20px;">
            Error Code: 404 Not Found
        </div>
        """ , 404
    



print(
    '''
     ██████╗ ██╗   ██╗██╗███╗   ██╗████████╗███████╗██╗  ██╗
    ██╔═══██╗██║   ██║██║████╗  ██║╚══██╔══╝██╔════╝╚██╗██╔╝
    ██║   ██║██║   ██║██║██╔██╗ ██║   ██║   █████╗   ╚███╔╝ 
    ██║▄▄ ██║██║   ██║██║██║╚██╗██║   ██║   ██╔══╝   ██╔██╗ 
    ╚██████╔╝╚██████╔╝██║██║ ╚████║   ██║   ███████╗██╔╝ ██╗
     ╚══▀▀═╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                                                  
    
                    By @krishaayjois21
                         v1.0.0
          https://github.com/krishaayjois21/Quintex
    '''
)
app.run(port=port,host='0.0.0.0')