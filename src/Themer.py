import flet as ft

STORAGE_KEY = "app_theme"

class ThemerMaster:
    def __init__(self, page: ft.Page, main_app):
        self.page = page
        self.main_app = main_app

        # self.light_theme = ft.Theme(
        #     color_scheme=ft.ColorScheme(
        #         primary="#34e0a0",
        #         on_primary="#2d2d2d",
        #         primary_container="#101010",
        #         background="#ffffff",
        #         secondary="#101010",
        #         on_secondary="#2a2a2a",
        #         tertiary="#f7f7f7",
        #         error="#e04c34",
        #     ),
        # )

        # self.dark_theme = ft.Theme(
        #     color_scheme=ft.ColorScheme(
        #         primary="#34e0a0",
        #         on_primary="#4c4c4c",
        #         primary_container="#101010",
        #         background="#000000",
        #         secondary="#f7f7f7",
        #         on_secondary="#2d2d2d",
        #         tertiary="#101010",
        #         error="#e04c34",
        #     ),
        # )
        
        self.theme_switch = ft.Switch(
            label="Theme Mode: ",
            label_position=ft.LabelPosition.LEFT,
            value=False,  # Initial value, will be updated by load_theme
            on_change=self.toggle_theme,
        )

        self.current_theme = self.load_theme()
        self.page.theme = self.load_theme()
        
        
    def load_theme(self):
        """Loads the last selected theme from client storage."""
        saved_theme = self.page.client_storage.get(STORAGE_KEY)
        if saved_theme == "dark":
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_switch.value = True
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_switch.value = False
        self.page.update()
        
        
        
    def toggle_theme(self, e):
        """Toggles the theme and saves the selection to client storage."""
        self.page.theme_mode = (
            ft.ThemeMode.DARK if not self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.LIGHT
        )
        self.page.client_storage.set(STORAGE_KEY, "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light")
        self.page.update()
        

    # def change_theme(self, e):
    #     self.current_theme = self.dark_theme if self.current_theme == self.light_theme else self.light_theme
    #     self.page.theme_mode = ft.ThemeMode.LIGHT if self.current_theme == self.light_theme else ft.ThemeMode.DARK
    #     self.page.update()

    #     self.page.bgcolor = self.current_theme.color_scheme.background
    #     self.main_app.update_views()
    #     self.main_app.dashboard.update()
    #     self.main_app.motors.update()
    #     self.main_app.clients.update()
    #     self.main_app.billing.update()
    #     self.main_app.settings.update()
    #     self.update_views_bg()
    #     self.page.update()

    # def change_theme_forced(self, theme):
    #     if theme == "light":
    #         self.current_theme = self.dark_theme
    #     elif theme == "dark":
    #         self.current_theme = self.light_theme
    #     else:
    #         return

    #     self.change_theme(None)

    # def update_views_bg(self):
    #     for i in range(len(self.page.views)):
    #         self.page.views[i].bgcolor = self.current_theme.color_scheme.background
    #         self.page.views[i].update()

    # def get_current_theme(self):
    #     if self.current_theme == self.light_theme:
    #         return "light"
    #     elif self.current_theme == self.dark_theme:
    #         return "dark"
    #     else:
    #         return None
        

