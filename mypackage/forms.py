from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    image_url = StringField('Image URL', validators=[Length(min=0, max=128)])
    website_url = StringField('Website URL', validators=[Length(min=0, max=128)])
    product_description = StringField('Product Description', validators=[Length(min=0, max=300)])
    cause_url = StringField('Cause URL', validators=[Length(min=0, max=128)])
    cause_description = StringField('Cause Description', validators=[Length(min=0, max=300)])
    submit = SubmitField('Load Company')
    
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    parent_id = StringField('Parent ID (0 if top level)', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Load Category')
    
class LinkForm(FlaskForm):
    company_id = IntegerField('Company ID', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField('Create Link')
    
class UnlinkForm(FlaskForm):
    company_id = IntegerField('Company ID', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField('Remove Link')