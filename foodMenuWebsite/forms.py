from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField,TextAreaField,IntegerField,DecimalField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length, NumberRange, ValidationError
from foodMenuWebsite.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    first_name =  StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name  = StringField('Last Name (Optional)', validators=[Optional(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    description = TextAreaField('Description', validators=[Length(max=750)])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Save Item')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max = 150)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Send Message')

class ReviewForm(FlaskForm):
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0,max=5)])
    comment = TextAreaField('Comment', validators=[Optional(),Length(max=2000)])
    submit = SubmitField('Submit Review')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    content = TextAreaField('Content', validators=[Optional(),Length(max=1000)])
    details = TextAreaField('More Details (Optional)', validators=[Optional(),Length(max=10000)])
    submit = SubmitField('Publish')

class UpdateAccountForm(FlaskForm):
    first_name =  StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name  = StringField('Last Name (Optional)', validators=[Optional(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg','webp'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Choose another one.')

class OrderForm(FlaskForm):
   food_item = StringField('Food Item', validators=[DataRequired(), Length(min=2)])
   quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
   submit = SubmitField('Submit')

class UpdateOrderStatusForm(FlaskForm):
    status = SelectField(
        "Order Status",
        choices=[
            ("Pending", "Pending"),
            ("Preparing", "Preparing"),
            ("Out for Delivery", "Out for Delivery"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Update Order Status')


