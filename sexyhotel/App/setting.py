# 配置文件
import os
class Config:
    SECRET_KEY = 'ucantguessit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = ''  # 邮箱服务器
    MAIL_USERNAME = ''  # 填邮箱
    MAIL_PASSWORD = ''  # 填授权码
    # 每页显示数据的条数
    PAGE_NUM = 5
# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG = True
    TESTING = False

# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG = False
    TESTING = True

# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG = False
    TESTING = False

# 配置字典：取别名
configDict = {
    'default':DevelopmentConfig,
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'Product':ProductionConfig
}