from nicegui import ui


def app_layout(content_function):
    """Verbessertes Layout"""

    # Header
    with ui.header().classes('bg-primary text-white p-4'):
        ui.label('Teilnehmerverwaltung').classes('text-xl')

    # Hauptcontainer
    with ui.row().classes('w-full h-screen'):
        # Navigation
        with ui.column().classes('bg-gray-100 w-64 h-full p-4'):
            ui.label('Navigation').classes('text-lg font-bold mb-4')
            ui.link('Home', '/').classes('text-blue-600 hover:text-blue-800 mb-2')
            ui.link('Andere Seite', '/other').classes('text-blue-600 hover:text-blue-800')

        # Inhaltsbereich
        with ui.column().classes('flex-1 p-4 overflow-auto'):
            content_function()  # Hier wird der Seiteninhalt gerendert