from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class PostsForm(FlaskForm):
    # PageDownField提供预览功能，如果想要设置字段的其它属性，可以通过render_kw完成
    content = PageDownField('今天想写点什么......', render_kw={'placeholder': '注意输入框下的格式预览，每行开头四个空格进入富文本编辑模式'}, validators=[DataRequired(), Length(1, 5000, message='评论字数不能超过5000')])
    submit = SubmitField('发表')


class CommentForm(FlaskForm):
    # 如果想要设置字段的其它属性，可以通过render_kw完成
    comment = PageDownField('', render_kw={'placeholder': '言论自由，友善评论......'},
                            validators=[DataRequired(), Length(1, 200, message='字数控制在200以内哦')])
    submit = SubmitField('发表评论')
