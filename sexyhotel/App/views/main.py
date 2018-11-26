from flask import Blueprint,render_template,request,current_app,redirect,url_for
from App.models import Posts
from sqlalchemy import or_,and_
from App.extensions import cache

main = Blueprint('main',__name__)
"""
@main.route('/index/')
@main.route('/')
@cache.memoize(timeout=30) #根据传参进行缓存 设置缓存日期为30秒
def index():
    # 获取页码
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    return redirect(url_for('main.show',page=page))


@main.route('/show/<int:page>/')
@cache.memoize(timeout=60)
def show(page):
    print('你能看到我几次？------------------------------------')
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,
                                                                                        current_app.config['PAGE_NUM'],
                                                                                        False)
    data = pagination.items  # 获取当前页面的数据
    return render_template('main/index.html', data=data, pagination=pagination)
"""






@main.route('/index/')
@main.route('/')
def index():
    # 获取页码
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1

    key = 'page'+str(page) #page1 page2...
    value = cache.get(key) #获取缓存
    if not value:
        print('没走缓存。。。。。。。。。。。。。。')
        pagination = Posts.query.filter_by(pid=0,state=True).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
        data = pagination.items #获取当前页面的数据
        value = render_template('main/index.html',data=data,pagination=pagination)
        cache.set(key,value,timeout=60) #设置缓存失效时间为1分钟

    return value #响应缓存内容


#清除缓存
@main.route('/clear_cache/')
def clear_cache():
    cache.clear()
    return redirect(url_for('main.index'))





"""
@main.route('/index/')
@main.route('/')
# @cache.cached(timeout=30) #设置缓存日期为30秒
@cache.memoize(timeout=30) #根据传参进行缓存 设置缓存日期为30秒
def index():
    print('你能看到我几次？------------------------------------')
    # 获取页码
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items #获取当前页面的数据
    return render_template('main/index.html',data=data,pagination=pagination)
"""

#博客搜索
@main.route('/search/',methods=['POST','GET'])
def search():
    # 获取页码
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1

    #获取搜索的内容
    if request.method == 'POST':
        word = request.form.get('search','')
    else:
        word = request.args.get('search','')

    pagination = Posts.query.filter(or_(Posts.title.contains(word),Posts.content.contains(word)),and_(Posts.pid==0,Posts.state==True)).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items  # 获取当前页面的数据
    return render_template('main/search_detail.html',data=data,pagination=pagination,word=word)
