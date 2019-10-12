"""Views, one for each mhacks page."""
from mhacks.views.index import show_index
from mhacks.views.login import login
from mhacks.views.logout import logout
from mhacks.views.create_user import create_user
from mhacks.views.edit import edit
from mhacks.views.delete import delete
from mhacks.views.password import password
from mhacks.views.static import show_image
from mhacks.views.explore import show_explore
from mhacks.views.follower import show_follower
from mhacks.views.following import show_following
from mhacks.views.user import show_user
from mhacks.views.post import show_post
from mhacks.views.home import home
