from flask import Blueprint, render_template, request, redirect, url_for
from controller.admin import getUsers, removeUser, updateUser, getTimes, getEsf, updateTimes, newEsf
from dao.paciente import getPacientes
from flask_login import login_required, LoginManager, current_user

menuAdmin = Blueprint('admin', __name__)

@menuAdmin.route('/admin', methods=['GET', 'POST'])
#@login_required
def admin():

    #if not current_user.supervisor:
    #    return redirect(url_for('MenuAtendente.index'))

    if request.method == 'POST':
        intervalo = request.form['intervalo']
        tempo_maximo = request.form['tempoMaximo']

        updateTimes(intervalo, tempo_maximo)

        return redirect(url_for('admin.admin'))

    elif request.method == 'GET':
        intervalo, tempo_maximo = getTimes() 
        
        esf=getEsf()

        users = getUsers()
        pacientes = getPacientes()

        return render_template('admin.html', users = users, pacientes = pacientes,
                                intervalo=intervalo, tempo_maximo=tempo_maximo, esf=esf)


@menuAdmin.route('/admin/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        id = request.form['user_id']

        removeUser(id)

    return redirect(url_for('admin.admin'))

@menuAdmin.route('/admin/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form['user_id']
        name = request.form['nome']
        crm = request.form['crm']
        cpf = request.form['cpf']                
        supervisor = 'supervisor' in request.form
        senha = request.form['senha']

        updateUser(id, name, crm, cpf, supervisor, senha)    

    return redirect(url_for('admin.admin'))

@menuAdmin.route('/admin/esf', methods=['POST'])
def addEsf():
    if request.method == 'POST':
        esf = request.form["esf"]

        newEsf(esf)

    return redirect(url_for('admin.admin'))