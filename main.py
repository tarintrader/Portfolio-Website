import os

from flask import Flask, render_template
from flask import flash, request
from flask_bootstrap import Bootstrap5
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
Bootstrap5(app)


class MyForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    resume = "static/CV_Adrian_Tarin.pdf"
    return render_template('index.html', resume=resume)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            # Send email
            subject = 'New Message from Your Website'
            sender_email = form.email.data
            message_body = f"Name: {form.name.data}\nEmail: {sender_email}\nMessage: {form.message.data}"

            msg = Message(subject, recipients=['adriantarinmartinez@gmail.com'], sender=sender_email)
            msg.body = message_body
            mail.send(msg)

            flash('Your message has been sent!', 'success')
        else:
            flash('All fields are required.', 'danger')

    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
