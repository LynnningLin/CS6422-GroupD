from flask_wtf import FlaskForm
from wtforms import ValidationError, IntegerField, SubmitField, BooleanField, SelectField
from wtforms.validators import InputRequired

class settingsForm(FlaskForm):
    target_temperature = IntegerField("Target Temperature",validators=[InputRequired()])
    occupation_detect = BooleanField("Occupation Detection")
    fire_alarm = BooleanField("Fire Alarm if Temp > 50 °C")
    mode = SelectField("Select your mode", choices=[('default', 'Default Mode'), ('economy', 'Economy Mode')])
    submit = SubmitField("Submit")