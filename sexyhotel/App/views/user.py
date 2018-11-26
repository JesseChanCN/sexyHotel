from flask import Blueprint, render_template, flash, redirect, url_for
from App.forms import Register,AgainActivate,Login# 导入注册表单类
from App.models import User # 导入User模型类
from werkzeug.security import  generate_password_hash,check_password_hash
from App.email import send_mail
from flask_login import login_required,logout_user,login_user,current_user
from datetime import datetime
from App.extensions import cache
user = Blueprint('user',__name__)
'''
1.接受到数据(用户名和邮箱唯一性)
2.保存到数据库(密码加密后的)
3.生成token值
4.配置发送邮件
5.发送激活邮件
6.提示用户注册成功 前去激活
7.跳转到登录页面
8.创建激活视图函数...
9.登录...
'''

# 注册
@user.route('/register/', methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        u = User(username=form.username.data, password=form.userpass.data, email=form.email.data)
        u.save()
        token = u.generate_token() # 生成token值
        send_mail('账户激活', u.email, 'activate', username=u.username, endpoint='user.activate', token=token)
        flash('恭喜注册成功 请去邮箱激活')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


#账户激活
@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('恭喜你激活成功  请登录')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败 请重新再次激活')
        return redirect(url_for('user.register'))


#再次激活
@user.route('/again_activate/',methods=['GET','POST'])
def again_activate():
    form = AgainActivate()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.userpass.data):
            flash('请输入正确的密码')
        elif u.confirm:
            flash('该账户已经激活 请前往登录')
        else:
            token = u.generate_token()  # 生成token值
            send_mail('账户激活', u.email, 'again_activate', username=u.username, endpoint='user.activate', token=token)
            flash('激活邮件发送成功 请前去邮箱进行激活')
            return redirect(url_for('user.login'))

    return render_template('user/again_activate.html', form=form)


#登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.userpass.data):
            flash('请输入正确的密码')
        elif not u.confirm:
            flash('该账户还没有激活 请激活后再次登录')
        else:
            u.lastLogin = datetime.utcnow()
            u.save()
            flash('登录成功！！！')
            login_user(u,remember=form.remember.data)
            return redirect(url_for('main.index'))
    return render_template('user/login.html', form=form)


#退出登录
@user.route('/logout/')
def logout():
    flash('退出成功')
    logout_user()
    cache.clear()
    return redirect(url_for('main.index'))

#必须登录才能访问
@user.route('/test/')
@login_required
def test():
    return 'test'

@user.route('/check/')
@login_required
def check():
    return render_template()