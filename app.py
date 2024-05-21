from flask import Flask, render_template, url_for, redirect, flash

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():  # put application's code here
    return render_template("index.html")


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


@app.route('/wie-wir-arbeiten', methods=['GET', 'POST'])
def wie_wir_arbeiten():
    return render_template("wie_wir_arbeiten.html")



@app.route('/kontrakt', methods=['GET', 'POST'])
def kontakt():
    return render_template("kontakt.html")




if __name__ == '__main__':
    app.run()
