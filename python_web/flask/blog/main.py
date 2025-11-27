from flask import Flask
from flask import render_template

#render template nos permite renderizar archivos html ubicados en la carpeta templates

app = Flask(__name__)

#variable que almacenara los posts que se vayan creando
posts = []

@app.route("/")
def index():
  return render_template("index.html", num_posts=len(posts))


@app.route("/p/<string:slug>")
def show_post(slug):
  return render_template("post_view.html", slug_title = slug)

@app.route("/admin/post")
@app.route("/admin7post/<int:post_id>/")
def post_form(post_id=None):
  return render_template("admin/post_form.html", post_id = post_id)

# @app.route("/")
# def index():
#   return"{} posts".format(len(posts))

#Para mostrar un post en particular debemos escribir /p/nombre-del-post en la url 
# @app.route("/p/<string:slug>")
# def show_post(slug):
#   return "Mostrando el post {} ".format(slug) 

# @app.route("/admin/post")
# @app.route("/admin/post/<int:post_id>")
# def post_form(post_id=None):
#   return"Post_form {}".format(post_id)
