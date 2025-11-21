from nicegui import ui
from lib.layout import app_layout

def page_other():
    def build():
        ui.label("Weitere Seite")
        ui.label("Hier kommt dein Inhalt hin.")

    app_layout(build)
