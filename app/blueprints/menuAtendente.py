from flask import Blueprint, render_template, current_app, jsonify
from flask_login import login_required, LoginManager, current_user
from datetime import datetime
from controller.pdfInclusao import incluiPdf
from blueprints.login import ler_dados

from dao.agendamento import userAgendamentos
from dao.paciente import getPaciente

menuAtendente = Blueprint('MenuAtendente', __name__)

@menuAtendente.route('/sw.js', methods=['GET'])
@login_required
def sw():
    return current_app.send_static_file('js/sw.js')

@menuAtendente.route('/', methods=['GET'])
@login_required 
def index():
    return render_template('menuAtendente.html', atendimentos = getAtendimentos(), formatTime = datetime.strftime, dados = ler_dados(), pdf = False, incluiBotaoPdf = incluiPdf())

@menuAtendente.route('/dados', methods=['GET'])
@login_required
def dados():
    agendamentos = getAtendimentos()
    return jsonify({
        "agendamentos" : agendamentos,
        "pacientes" : [getPaciente(ag['idPaciente']).to_dict() for ag in agendamentos]
    
    }), 200

def setImportance(atendimento):
    today = datetime.today().date()
    time = atendimento['diaAgendamento'].date()
    
    if(today > time):
        atendimento['importance'] = 1
    elif(today == time):
        atendimento['importance'] = 2
    else:
        atendimento['importance'] = 3
    
    return atendimento

def getAtendimentos():
    return list(map(
        setImportance, 
        userAgendamentos(current_user.id)))
