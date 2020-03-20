from app.extensions import db
from datetime import datetime
from markdown import markdown
import bleach


class Posts(db.Model):
    __tablesname__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)          # 定义回复几号的贴子，默认为0(发送的)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))      # 外键
    content_html = db.Column(db.Text)                           # 渲染后的HTML格式内容

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.content_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Posts.content, 'set', Posts.on_changed_content)        # 监听输入框内的新字段，将其渲染成HTML格式
