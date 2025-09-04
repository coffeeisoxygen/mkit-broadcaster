from views.pages.broadcast import broadcast_page
from views.pages.dashboard import dashboard_page
from views.pages.profile import profile_page
from views.pages.settings import settings_page

PAGES = [
    ("Dashboard", dashboard_page),
    ("Broadcast", broadcast_page),
    ("Settings", settings_page),
    ("Profile", profile_page),
]
