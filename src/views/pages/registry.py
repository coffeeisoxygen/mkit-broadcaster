import flet as ft

from views.pages.broadcast import broadcast_page
from views.pages.dashboard import dashboard_page
from views.pages.profile import profile_page
from views.pages.settings import settings_page

# Single source of truth for page definitions
PAGE_DEFS = [
    {"name": "Dashboard", "icon": ft.Icons.HOME, "view": dashboard_page},
    {"name": "Broadcast", "icon": ft.Icons.SEND, "view": broadcast_page},
    {"name": "Settings", "icon": ft.Icons.SETTINGS, "view": settings_page},
    {"name": "Profile", "icon": ft.Icons.PERSON, "view": profile_page},
]

# Registry for navigation and page switching
PAGES = [(p["name"], p["view"]) for p in PAGE_DEFS]

# Sidebar destinations for NavigationRail
SIDEBAR_DESTINATIONS = [
    ft.NavigationRailDestination(icon=p["icon"], label=p["name"]) for p in PAGE_DEFS
]
