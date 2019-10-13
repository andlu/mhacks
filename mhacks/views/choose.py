"""
mhacks Edit View.

URLs include:
/choose/
"""
import os
import flask
from mhacks.model import get_db
import mhacks


# displays all possible playlists, returns unique identifier of chosen playlist 
@mhacks.app.route('/choose/', methods=['GET', 'POST'])
def choose(sp):
    sp     
