from flet import *
from MainApp import MainApp

def main(page: Page):
    MainApp(page, "Allo Casse Auto", "./logo/mallouka_motors_logo.png")
    page.update()

app(target=main, assets_dir="assets")

