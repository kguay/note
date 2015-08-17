# errors.py renders pages for 404 and 500 errors.

# flask
from flask import render_template
# local
from . import main

# 404 (not found) error page
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 500 (server error) page
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
