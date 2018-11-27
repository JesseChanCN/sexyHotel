from flask import Blueprint,render_template,request,current_app,redirect,url_for
from sqlalchemy import or_,and_
from App.extensions import cache

