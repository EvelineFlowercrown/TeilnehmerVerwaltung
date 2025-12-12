import os

from nicegui import ui
from lib.pages.home import page_home
from lib.pages.other import page_other

def create_app():

    @ui.page('/')
    async def home_page():
        page_home()

    @ui.page('/other')
    async def other_page():
        page_other()

    port = int(os.getenv("PORT", 8080))
    ui.run(host='0.0.0.0', port=port,title="Teilnehmerverwaltung")
