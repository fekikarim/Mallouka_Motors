from flet import *
from routes import Routes
from Dashboard import Dashboard
from Motors import Motors
from Clients import Clients
from Billings import Billings
from Settings import Settings
from Themer import ThemerMaster
from app_bar import AppBarMaster

class MainApp:
    def __init__(self, page: Page, APP_NAME: str, APP_LOGO_PATH: str):
        self.page = page
        self.APP_NAME = APP_NAME
        self.APP_LOGO_PATH = APP_LOGO_PATH
        
        self.page.title = self.APP_NAME
        self.page.window.icon = APP_LOGO_PATH

        self.themer = ThemerMaster(self.page, self)

        self.dashboard = Dashboard(self.page, self, self.themer)
        self.motors = Motors(self.page, self, self.themer)
        self.clients = Clients(self.page, self, self.themer)
        self.billing = Billings(self.page, self, self.themer)
        self.settings = Settings(self.page, self, self.themer)
        
        self.ub = AppBarMaster(self.page, self, self.themer, self.APP_NAME, Icons.DASHBOARD)

        # page configuration
        # self.page.theme_mode = ThemeMode.DARK
        self.page.adaptive = True
        # self.page.bgcolor = self.page.theme.color_scheme.background
        self.page.padding = 15

        # make frames
        # self.make_frames()
        # self.page.update()

        self.router = Routes(self.page, self)
        
        self.themer.load_theme()
        
        self.page.go("/")

    # def update(self):
    #     self.page.update()
    #     self.update_views()
    #     self.dashboard.update()
    #     self.motors.update()
    #     self.clients.update()
    #     self.billing.update()
    #     self.settings.update()
    #     self.page.update()

    # def change_theme(self, e):
    #     self.themer.change_theme(e)

    # def make_frames(self):
    #     self.dashboard_frame = self.dashboard.dashboard_frame
    #     self.motors_frame = self.motors.motors_frame
    #     self.clients_frame = self.clients.clients_frame
    #     self.billing_frame = self.billing.billing_frame
    #     self.settings_frame = self.settings.settings_frame

    # def update_views(self):
    #     for i in range(len(self.page.views)):
    #         try:
    #             self.page.views[i].appbar.update()
    #         except:
    #             pass
    #         self.page.views[i].bgcolor = self.themer.current_theme.color_scheme.background
