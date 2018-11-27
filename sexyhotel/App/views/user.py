from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.security import  generate_password_hash,check_password_hash
from App.email import send_mail
from flask_login import login_required,logout_user,login_user,current_user
from datetime import datetime
from App.extensions import cache
