from flet import *
from MainApp import MainApp
from db import *
import os

def main(page: Page):
    MainApp(page, "Mallouka Motors", "./logo/mallouka_motors_logo.png")
    page.update()    

app(target=main, assets_dir="assets")

