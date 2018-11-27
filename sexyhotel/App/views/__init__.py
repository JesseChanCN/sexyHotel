from .main import main # 首页蓝本
from .user import user # 用户处理的蓝本对象
from .posts import posts
from .owncenter import center

blueprintConfig = [

]
# 注册蓝本
def register_blueprint(app):
    for blueprint, prefix in blueprintConfig:
        app.register_blueprint(blueprint, url_prefix=prefix)