import os


base_dir = os.path.abspath(os.path.dirname(__name__))  # 获取当前环境目录


# 通用配置
class Config:
    # 密钥禁止使用中文
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True     # 自动提交，不需要每次都commit()
    SQLALCHEMY_TRACK_MODIFICATIONS = False   # 取消追踪
    # 邮件配置
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '1124882400@qq.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'jrcnxgvzcoujbada'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '1124882400@qq.com'
    MAIL_PASSWORD = 'jrcnxgvzcoujbada'  # 授权码不能用空格
    # app.config['MAIL_DEFAULT_SENDER'] = '1124882400@qq.com'  # 默认的邮件发送者
    # 使用本地库中的bootstrap依赖包
    BOOTSTRAP_SERVER_LOCAL = True
    # 文件上传
    MAX_CONTENT_LENGTH = 16*1024*1024      # 最大上传16M
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'app/static/upload')     # 上传文件存储路径

    # 初始化的方法
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog_dev'


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog_test'


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认配置为开发环境
    'default': DevelopmentConfig
}