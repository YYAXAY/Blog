from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer    # 邮件激活使用
from app.forms import PostsForm
from app.models import Posts, User
from flask_login import current_user
from app.extensions import db


# 创建蓝本
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            # 根据表单提交数据创建对象
            p = Posts(content=form.content.data, user=u)
            # 写进数据库
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('请登陆后再发表')
            return redirect(url_for('user.login'))
    # 从数据库中读取博客，并分配到模板中，然后在模板中渲染
    # 按时间排序，最后发表的显示在首页，并且只获取发表的博客，过滤回复的
    # posts = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
    # 分页处理，获取当前页码，没有认为是第一页,每页设置为10条
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)


# 或取搜索框内容,为空则回首页
@main.route('/search', methods=['POST'])
def search():
    if not request.form['search']:
        flash('搜索框为空！')
        return redirect(url_for('.index'))
    return redirect(url_for('.search_results', query=request.form['search']))


# 搜索内容
@main.route('/search_results/<query>')
def search_results(query):
    page = request.args.get('page', 1, type=int)
    pagination_u = User.query.filter(User.username.contains(query)).paginate(page, per_page=5, error_out=False)    # 模糊查找所有相关用户
    pagination_p = Posts.query.filter(Posts.content.contains(query), Posts.rid == 0).paginate(page, per_page=10, error_out=False)  # 模糊查找相关贴子
    users = pagination_u.items
    results = pagination_p.items
    return render_template('/main/search_results.html', query=query, users=users, results=results, pagination_u=pagination_u, pagination_p=pagination_p)


# 加密路由
@main.route('/jiami/')
def jiami():
    return generate_password_hash('123456')


# 密码校验
@main.route('/check/<password>')
def check(password):
    # 密码校验函数参数（加密后的值，密码）
    # 正确返回：True,错误返回：False
    if check_password_hash('pbkdf2:sha256:150000$EOcyqjLb$b46660d325b46e5ed21833dcb19caeb66f78e37ff4f48e973490b04ccf6c8c89', password):
        return '密码正确'
    else:
        return '密码错误'


# 邮箱验证
@main.route('/generate_token/')
def generate_token():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)  # 指定密钥过期时间
    # 加密指定的数据以字典的形式传入
    return s.dumps({'id': 250})


# 邮箱返回校验
@main.route('/activate/<token>')
def activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except Exception as e:
        print(e)
        return 'token有误'
    return str(data.get('id'))


