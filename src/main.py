from flet import *
from MainApp import MainApp

def main(page: Page):
    MainApp(page, "Allo Casse Auto", "./allo_casse_auto_logo.jpg")
    page.update()

app(target=main, assets_dir="assets")

