from nicegui import ui
from lib.pages.home import page_home
from lib.pages.other import page_other

def create_app():

    @ui.page('/')
    def home_page():
        page_home()

    @ui.page('/other')
    def other_page():
        page_other()

    ui.run(title="Teilnehmerverwaltung")
