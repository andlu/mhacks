"""
mhacks Create View.

URLs include:
/accounts/create/
"""
import flask
from mhacks.model import get_db
import mhacks
from mhacks.views.accountfunctions import file_upload, hash_function


@mhacks.app.route('/accounts/create/', methods=['GET', 'POST'])
def create_playlist():
    