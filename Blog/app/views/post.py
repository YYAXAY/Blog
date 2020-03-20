from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.models import User, Posts
from app.forms import CommentForm
from app.extensions import db
from flask_login import current_user


# 创建蓝本
post = Blueprint('post', __name__)


# 文章详情
@post.route('/post_detail/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    post = Posts.query.filter_by(id=id).first()            # 获取当前点击的博客内容
    form = CommentForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            # 根据表单提交数据创建对象
            p = Posts(content=form.comment.data, uid=post.user.id, rid=id, user=u)
            # 写进数据库
            db.session.add(p)
            return redirect(url_for('post.post_detail', id=id))
        else:
            flash('请登陆后再评论')
            return redirect(url_for('user.login'))
    # comments = Posts.query.filter_by(rid=id).all()
    # 从数据库中读取博客，并分配到模板中，然后在模板中渲染
    # 按时间排序所有评论，并分页处理，获取当前页码，没有认为是第一页,每页设置为5条
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=id).order_by(Posts.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    comments = pagination.items
    return render_template('post/post_detail.html', form=form, post=post, comments=comments, pagination=pagination)


# 查看某位用户所有博客
@post.route('/post_personal/<int:uid>', methods=['GET', 'POST'])
def post_personal(uid):
    user_p = User.query.filter_by(id=uid).first()
    # post = Posts.query.filter_by(rid=0, uid=uid).order_by(Posts.timestamp.desc()).all()
    # 分页展示该用户所有贴子
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0, uid=uid).order_by(Posts.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('post/post_personal.html', posts=posts, user_p=user_p, pagination=pagination)

