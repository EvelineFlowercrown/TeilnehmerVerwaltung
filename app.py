# app.py
from nicegui import ui
from typing import Type, Any
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from database import SessionLocal, engine, BaseClass
import models  # deine models.py mit Klassen importiert


with ui.row():
    ui.label("hello world")
    ui.label("this is")
    ui.label("hello world")
ui.run()
