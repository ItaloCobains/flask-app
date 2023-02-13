from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('funcionarios', __name__)


@bp.route('/funcionarios')
def index():
    db = get_db()
    funcionarios = db.execute(
        'SELECT * FROM funcionarios'
        ' ORDER BY created DESC').fetchall()
    return render_template('funcionarios/index.html', funcionarios=funcionarios)


@bp.route('/funcionarios/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        cargo = request.form['cargo']
        salario = request.form['salario']
        error = None

        if not nome:
            error = 'Nome é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO funcionarios (nome, cpf, endereco, telefone, email, cargo, salario)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (nome, cpf, endereco, telefone, email, cargo, salario)
            )
            db.commit()
            return redirect(url_for('funcionarios.index'))

    return render_template('funcionarios/create.html')


def get_funcionario(id, check_author=True):
    funcionario = get_db().execute(
        'SELECT *'
        ' FROM funcionarios'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    if funcionario is None:
        abort(404, f"Funcionário id {id} não existe.")

    if check_author and funcionario['author_id'] != g.user['id']:
        abort(403)


@bp.route('/funcionarios/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id: int):
    funcionario = get_funcionario(id)

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        cargo = request.form['cargo']
        salario = request.form['salario']
        error = None

        if not nome:
            error = 'Nome é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE funcionarios SET nome = ?, cpf = ?, endereco = ?, telefone = ?, email = ?, cargo = ?, salario = ?'
                ' WHERE id = ?',
                (nome, cpf, endereco, telefone, email, cargo, salario, id)
            )
            db.commit()
            return redirect(url_for('funcionarios.index'))

    return render_template('funcionarios/update.html', funcionario=funcionario)


@bp.route('/funcionarios/<int:id>/delete', methods=('POST',))
@login_required
def delete(id: int):
    get_funcionario(id)
    db = get_db()
    db.execute('DELETE FROM funcionarios WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('funcionarios.index'))
