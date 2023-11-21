from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db 
from app.modelos.cliente import Cliente 
from app.common.sql_utils import SqlUtils
from app.modelos.venta import Venta
from sqlalchemy import or_ , func
import fpdf
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi



api_reporteVentas = Blueprint('api_reporteVentas', __name__, url_prefix='/api/reportes/reporteVentas')