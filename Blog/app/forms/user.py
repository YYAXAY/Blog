#导入表单基类
from flask_wtf import FlaskForm
# 导入相关字段
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
# 导入验证器类
from wtforms.validators import DataRequired, EqualTo, Email, Length
from app.models import User
# 导入上传文件的字段及验证器
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.extensions import photos


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(2, 10, message='用户名必须在2-10个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 16, message='密码长度需要在6-16位之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 自定义验证器，验证用户名
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在')

    # # 自定义验证器，验证邮箱
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册过')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('立即登录')


# 修改密码表单
class PasswordForm(FlaskForm):
    old_pwd = PasswordField('原密码', validators=[DataRequired()])
    new_pwd = PasswordField('新密码', validators=[DataRequired(), Length(6, 16, message='密码长度需要在6-16位之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('new_pwd', message='两次密码不一致')])
    submit = SubmitField('确认修改')


# 修改邮箱表单
class EmailForm(FlaskForm):
    old_email = StringField('原邮箱', validators=[Email(message='邮箱格式不正确')])
    new_email = StringField('新邮箱', validators=[Email(message='邮箱格式不正确')])
    confirm = StringField('确认邮箱', validators=[EqualTo('new_email', message='两次邮箱地址不一致')])
    submit = SubmitField('确认修改')


# 修改头像表单
class IconFrom(FlaskForm):
    iocn = FileField('头像', validators=[FileRequired('请选择上传文件'), FileAllowed(photos, '只能上传图像')])
    submit = SubmitField('上传')
