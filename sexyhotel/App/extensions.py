from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager #登录处理扩展库
from flask_cache import Cache #缓存模块

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE':'simple'})
# cache = Cache(config={'CACHE_TYPE':'redis'})

# 初始化所有第三方扩展库加载
def ext_init(app):
    bootstrap.init_app(app) # bootstrap
    moment.init_app(app) # 格式化时间的扩展库
    db.init_app(app) # 模型的对象
    migrate.init_app(app) # 模型迁移对象
    mail.init_app(app)
    cache.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login' # 指定登录的端点
    login_manager.login_message = '请先登录后再进行访问' # 跳到登录后显示的用户信息
    login_manager.session_protection = 'strong' # 设置session保护级别