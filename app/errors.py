from flask import render_template
from app import app


@app.errorhandler(400)
def bad_request(error):
    return render_template('error/400.html', title="Ошибка"), 400


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html', title="Ошибка"), 404


@app.errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template('error/500.html', title="Ошибка"), 500
