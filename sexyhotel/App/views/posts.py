from flask import Blueprint,render_template,flash,redirect,url_for,request,jsonify
from App.forms import Posts
from App.models import Posts as MPosts
from flask_login import current_user

posts = Blueprint('posts',__name__)

#发表博客
@posts.route('/send_posts/',methods=['GET','POST'])
def send_posts():
    form = Posts()
    if not current_user.is_authenticated:
        flash('您还没有登录 请先登录在发表')
    elif form.validate_on_submit():
        p = MPosts(title=form.title.data,content=form.content.data,user=current_user)
        p.save()
        flash('发表成功！去首页进行查看')
        return redirect(url_for('posts.send_posts'))
    return render_template('posts/send_posts.html',form=form)



#博客详情
@posts.route('/posts_detail/<int:pid>/')
def posts_detail(pid):
    form = Posts() #作为评论和回复的表单类样式
    data = MPosts.query.get(pid)
    comment = MPosts.query.filter(MPosts.path.contains(str(pid))).order_by(MPosts.path.concat(MPosts.id))
    #select * from posts where path like '%pid%' order by concat(path,id)
    return render_template('posts/posts_detail.html',data=data,comment=comment,form=form)


#添加评论和回复视图函数
@posts.route('/comment/',methods=['POST'])
def comment():
    pid = int(request.form.get('pid')) #博客的自增id
    rid = int(request.form.get('rid',0)) #回复评论人的id
    if current_user.is_authenticated:
        if rid:
            ppid = rid
        else:
            ppid = pid
        p = MPosts.query.get(ppid)
        MPosts(content=request.form.get('content'),pid=ppid,path=p.path+str(p.id)+',',user=current_user).save()
    else:
        flash('请先登录在发表评论')
    return redirect(url_for('posts.posts_detail', pid=pid))

#收藏操作
@posts.route('/dofavorite/')
def doFavorite():
    try:
        pid = int(request.args.get('pid'))
        if current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
        else:
            current_user.add_favorite(pid)
        return jsonify({'code': 200})
    except:
        return jsonify({'code':500})