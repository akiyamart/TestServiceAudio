from sqladmin import Admin

from .security import authentication_backend
from ..db.engine import engine
from .views import (
    UserView, 
)
        
def setup_admin(app):
    admin = Admin(
        app=app, 
        engine=engine,
        title="Audio-Service Admin", 
        base_url="/admin", 
        debug=True,
        authentication_backend=authentication_backend
    )
    admin.add_view(UserView)
