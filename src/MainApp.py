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
        self.page.adaptive = True
        self.page.padding = 15



        self.router = Routes(self.page, self)
        
        self.themer.load_theme()
        
        self.page.go("/")


