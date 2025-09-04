class AppState:
    """Centralized application state for session, navigation, and user info.
    Extendable for more features (e.g., settings, broadcast, etc).
    """

    def __init__(self):
        self.is_logged_in: bool = False
        self.user: dict | None = None

    def login(self, user_info: dict):
        self.is_logged_in = True
        self.user = user_info

    def logout(self):
        self.is_logged_in = False
        self.user = None

    # Extend with more state and methods as needed


# Singleton instance for global access
app_state = AppState()
