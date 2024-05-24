from flask import Flask, render_template, url_for, redirect, flash, request
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import DataRequired, Email

from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, InputRequired
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm, RegisterForm, LoginForm, BlogPostForm
from flask_ckeditor import CKEditor
import json
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from waitress import serve
import dns.resolver

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'geheim'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

bootstrap = Bootstrap5(app)

login_manager = LoginManager()

login_manager.init_app(app)


# IP 192.168.10.31

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique= True, nullable=False)
    email = db.Column(db.String(120), unique= True, nullable=False)
    password = db.Column(db.String(200), unique= True, nullable=False)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    image = db.Column(db.String(200), nullable=False)


class ContactFormsData(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    mobile_phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.String(400), nullable=False)

with app.app_context():
    db.create_all()


smtp_server = 'smtp.awb-it.de'
port = 25

#sender_email = "werner.boehme@awb-it.de"
sender_email = "werner.boehme@awb-it.de"
receiver_email = "stefan.boehme@awb-it.de"
password = "@@AnStWe20"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def start():  # put application's code here
    return render_template("start.html")


@app.route("/starter-page", methods=["GET", "POST"])
def starter_page():
    return render_template("starter-page.html")

@app.route('/leistungen', methods=['GET', 'POST'])
def leistungen():
    return render_template("leistungen.html")


@app.route('/über-uns', methods=['GET', 'POST'])
def über_uns():

    return render_template("über_uns.html")

@app.route('/blog', methods=['GET', 'POST'])
def blog_overview():
    blog_content_first_sentences = []

    blog_posts = Posts.query.all()



    for post in blog_posts:
        first_sentences = post.content.split(".")[:2]
        print(f"Ersten Sätze: {first_sentences}")
        blog_content_first_sentences.append(first_sentences)

    print(f"Gsamet Blogcontentnfirstsentences: {blog_content_first_sentences}")



    return render_template("blog_overview.html", blog_posts = blog_posts, blog_content_first_sentences = blog_content_first_sentences)


@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def blog_post(post_id):

    post = Posts.query.get(post_id)

    return render_template("blog_post.html", blog_post_content = post.content, blog_post_title = post.title, blog_post_image = post.image, blog_post_date = post.date, blog_post_subtitle = post.subtitle)




@app.route('/wie-wir-arbeiten', methods=['GET', 'POST'])
def wie_wir_arbeiten():
    return render_template("wie_wir_arbeiten.html")



@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == "POST":

        if request.form["name"] == "" or request.form["email"] == "" or request.form["company"] == "" or request.form[
            "mobil"] == "" or request.form["question"] == "":
            flash("Füllen Sie alle Pflichtfelder aus")
            print(request.form["name"], request.form["email"], request.form["company"], request.form["phone_number"])

            return redirect(url_for("contact"))


        # elif not isinstance(request.form["mobil"], (int)) or not isinstance(request.form["phone_number"], (int)) or request.form["phone_number"] == None or request.form["mobil"] == None:
        # flash("Geben Sie eine gültige Telefonnumer an")
        # return redirect(url_for("contact"))"""

        else:

            name = request.form["name"]
            email = request.form["email"]
            company = request.form["company"]
            phone_number = request.form["phone_number"]
            mobil = request.form["mobil"]
            question = request.form["question"]

            if not check_email_domain(email):
                flash(f"Die Domain der E-Mail '{email}' existiert nicht")
                return redirect(url_for("contact"))

            new_contact_data = ContactFormsData(
                name=name,
                email=email,
                company=company,
                phone_number=phone_number,
                mobile_phone_number=mobil,
                question=question
            )

            db.session.add(new_contact_data)
            db.session.commit()

            # Email senden an Kunden
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = email
                message["Subject"] = " Bestätigung Ihrer Anfrage"

                body = f"""Sehr geehrte(r) {name},\n
    Wir möchten Ihnen bestätigen, dass wir Ihre Anfrage erhalten haben und diese derzeit bearbeiten. Unser Team wird sich in Kürze mit Ihnen in Verbindung setzen, um weitere Informationen bereitzustellen oder um den Fortschritt Ihrer Anfrage mitzuteilen. Wir schätzen Ihr Interesse und Ihr Vertrauen in AWB-IT. Bitte zögern Sie nicht, sich bei weiteren Fragen oder Anliegen an uns zu wenden.

    Mit freundlichen Grüßen,
    Ihr AWB-Team"""

                message.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP(smtp_server, port) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, email, message.as_string())

                print("E-Mail sent.")


            except Exception as e:
                print(e)

            # Email senden an sich selber
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = sender_email
                message["Subject"] = " Neue Benutzeranfrage an Anfrage an AWB-IT (Website)"

                body = f"""\n\n\nName: {name}
                                Email: {email}
                                Firma: {company}
                                Mobilnummer: {mobil}
                                Telefonnummer: {phone_number}
                                Anfrage: {question}
                                """

                message.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP(smtp_server, port) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, sender_email, message.as_string())

                print("E-Mail sent.")

            except Exception as e:
                print(e)


            return redirect(url_for('start'))

    return render_template("kontakt.html")





@app.route('/testseite')
def testseite():
    return render_template("testseite.html")



@app.route('/blogpost-erstellen', methods=['GET', 'POST'])
def blog_post_erstellen():

    blog_post_form = BlogPostForm()

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    else:

        if blog_post_form.validate_on_submit():
            date_today = datetime.datetime.today().strftime("%d %b %Y")

            new_blog_post = Posts(title=blog_post_form.title.data, date = str(date_today), subtitle = blog_post_form.subtitle.data, content=blog_post_form.content.data, image=blog_post_form.image.data)
            db.session.add(new_blog_post)
            db.session.commit()

            return redirect(url_for("blog_overview"))


    return render_template("create_blog.html", blog_post_form = blog_post_form)










@app.route("/login", methods = ["GET", "POST"])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == login_form.password.data:
                login_user(user)
                return redirect(url_for("blog_post_erstellen"))
            else:
                flash("Passwort ist falsch")
                return redirect(url_for("login"))

        else:
            flash("Benutzername existiert nicht")
            return redirect(url_for("login"))


    return render_template("login.html", login_form = login_form)


def check_email_domain(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except :
        return False


@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")

@app.route("/cookies")
def cookies():
    return render_template("cookies.html")




if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=5077, threads=1)
