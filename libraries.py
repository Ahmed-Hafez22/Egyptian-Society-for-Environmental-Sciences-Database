# Libraries 
import pandas as pd
from sqlite3 import *
from os import *
from datetime import *
from tabulate import *
from arabic_reshaper import *
from bidi import *
from re import *
from fastapi import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
from typing import List, Optional
import io
from pydantic import *
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from time import sleep
import requests
import builtins
from tkinter import ttk