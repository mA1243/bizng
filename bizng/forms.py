from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, PasswordField, TelField, SelectField, SearchField,  HiddenField
from wtforms.validators import Email, DataRequired, EqualTo
from flask_wtf.file import FileAllowed, FileField, FileRequired
from bizng.models import State, Category, LGA

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Enter your name")])
    email = EmailField("Email", validators=[DataRequired(message="Enter your email"), Email(message="Enter email with proper formatting")])
    subject = StringField("Subject", validators=[DataRequired(message="Enter subject")])
    message = TextAreaField("Message", validators=[DataRequired(message="Enter a message")])
    submit = SubmitField("Submit")
    
class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    change_password = PasswordField("Change Password", validators=[])
    confirm_change_password = PasswordField("Confirm Password", validators=[EqualTo("change_password")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Confirm Password")])
    register = SubmitField("Register")
    confirm = SubmitField("Confirm")
    dp = FileField("Display Picture", validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")])

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="Enter your email"), Email(message="Enter email with proper formatting")])
    password = PasswordField("Password", validators=[DataRequired(message="Enter your password")])
    login = SubmitField("Login")
    
class ListingForm(FlaskForm):
    name = StringField("Business Name", validators=[DataRequired(message="Enter business name")])
    email = EmailField("Business Email", validators=[DataRequired(message="Enter business email"), Email(message="Enter email with proper formatting")])
    phoneno = TelField("Phone Number", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    category = SelectField("Category", choices=[], validators=[DataRequired()])
    website = StringField("Website")
    state = SelectField("State", choices=[], validators=[DataRequired()])
    lga = SelectField("Local Government Area", choices=[], validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired(message="Enter your address")])
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])
    businessimg = FileField("Business Image", validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")])
    submit = SubmitField("Publish Listing")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate state choices from the State table
        self.state.choices = [(state.id, state.name) for state in State.query.all()]
        # Populate category choices from the Category table
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
        
        # Initialize LGA choices with an empty list
        self.lga.choices = []
        
        # If state_id is provided in the form data, populate LGA choices
        if 'state_id' in kwargs and kwargs['state_id']:
            state_id = kwargs['state_id']
            self.lga.choices = [(lga.id, lga.name) for lga in LGA.query.filter_by(state_id=state_id).all()]
        
    def set_lga_choices(self, state_id):
        """Update LGA choices based on selected state"""
        self.lga.choices = [(lga.id, lga.name) for lga in LGA.query.filter_by(state_id=state_id).all()]

class SearchForm(FlaskForm):
    
    query = SearchField("Query")
    category = SelectField("Category", choices=[])
    state = SelectField("State", choices=[])
    lga = SelectField("Local Government Area", choices=[])
    search = SubmitField("Search")
    filter = SubmitField("Filter")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.state.choices = [(state.id, state.name) for state in State.query.all()]
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
        
class ReviewForm(FlaskForm):
    name = StringField("Fullname", validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Review")
    
class ReportForm(FlaskForm):
    report_type = HiddenField("Report Type", validators=[DataRequired()])
    report_id = HiddenField("Report ID", validators=[DataRequired()])
    reason = SelectField(
        "Reason",
        choices=[
            ("", "Select a reason..."),
            ("inappropriate", "Inappropriate Content"),
            ("spam", "Spam"),
            ("fake", "Fake Business/Review"),
            ("offensive", "Offensive Content"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )
    details = TextAreaField(
        "Details",
        validators=[DataRequired()],
        render_kw={"rows": 4, "placeholder": "Please provide specific details about your report..."},
    )
    submit = SubmitField("Submit Report")