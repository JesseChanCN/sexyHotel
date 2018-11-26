from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from App.extensions import cache
from App.models import Posts as MPosts # 模型名
from App.forms import Posts # 表单类名
center = Blueprint('center', __name__)

# 博客管理
@center.route('/blog_manage/')
@login_required
def blog_manage():
    data = current_user.posts.filter_by(pid=0).order_by(MPosts.timestamp.desc())
    # print(data.all())
    return render_template('owncenter/blogmanage.html', data=data)


# 博客编辑
@center.route('/edit_blog/<int:pid>/',methods=['GET', 'POST'])
def edit_blog(pid):
    form = Posts()
    posts = MPosts.query.get(pid) # 查询出 博客id对应的博客数据
    if form.validate_on_submit():
        posts.title = request.form.get('title')
        posts.content = request.form.get('content')
        posts.timestamp = datetime.utcnow()
        posts.save()
        flash('博客更新成功')
        cache.clear()
        return redirect(url_for('center.blog_manage'))
    # 给表单添加默认值
    form.title.data = posts.title
    form.content.data = posts.content
    return render_template('owncenter/edit_blog.html', posts=posts, pid=pid, form=form)

@center.route('/see_myself/<int:pid>/')
def see_myself(pid):
    posts = MPosts.query.get(pid) # 查询出博客id对应的博客数据
    posts.state = not posts.state
    posts.save()
    flash('设置成功！')
    cache.clear()
    return redirect(url_for('center.blog_manage'))

# 删除
@center.route('/del_posts/<int:pid>/')
def del_posts(pid):
    posts = MPosts.query.get(pid) #查询出 博客id对应的博客数据
    posts.delete()
    flash('删除成功！')
    cache.clear()
    return redirect(url_for('center.blog_manage'))

# 我的收藏
@center.route('/collections/')
@login_required
def collections():
    try:
        pid = int(request.args.get('pid'))
        if pid and current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
            flash("取消收藏成功！")
            return redirect(url_for('center.collections'))
    except:
        pass
    data = current_user.favorites.all()  # 查询所有的收藏
    return render_template('owncenter/collections.html',data=data)