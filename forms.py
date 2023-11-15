from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    publication_year = StringField('Publication Year', validators=[DataRequired()])
