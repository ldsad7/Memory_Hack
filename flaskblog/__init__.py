import paramiko

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SECRET_KEY'] = '203ad5ffa1d7c650ad681fdff3965cd2'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

####### SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('0.tcp.ngrok.io', username='root', password='U41p6CULJcTiUBEL0I023sCESb7hBe', port=11804)

ssh.exec_command("python3 -m pip install -r /content/DeOldify/colab_requirements.txt")
ftp = ssh.open_sftp()
#######

from flaskblog import routes
