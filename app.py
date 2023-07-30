from flask import (
    Flask,
    request,
    make_response,
    render_template,
    session,
    redirect,
    url_for,
    flash,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from functions import remove_non_alphabetical, suggestion


table_dico = {"lucas bensaid": "Mojito", "ilana cohen": "Negroni", "sacha farsy": "Gin Tonic", "jean-pierre benichou": "Margarita",
"noémie attal": "Old Fashioned", "benjamin akoun": "Old Fashioned"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "fbcfjnj3r948334i23ejd2mewx"
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    firstname = StringField("Prénom", validators=[DataRequired()])
    name = StringField("Nom", validators=[DataRequired()])
    submit = SubmitField("Click")


@app.route("/", methods=["GET", "POST"])
def index():
    # name = None
    form = NameForm()

    if form.validate_on_submit():
        session["firstname"] = form.firstname.data
        session["name"] = form.name.data
        session["full_name"] = (
            remove_non_alphabetical(session["firstname"])
            + " "
            + remove_non_alphabetical(session["name"])
        )
        session["attempt"] = session.get("attempt", 0) + 1
        session["form_validated"] = False
        session["suggestion_lst"] = False

        if session["full_name"] in table_dico:
            session["table"] = table_dico[session["full_name"]]
            session["form_validated"] = True
            return redirect(url_for("my_table", table=session["table"]))

        else:
            flash(
                f"Le <strong>Prénom:</strong> <em>{session['firstname']}</em> et le <strong>Nom:</strong> <em>{session['name']}</em> n'ont pas été trouvés."
            )

            session["suggestion_lst"] = suggestion(session['full_name'], table_dico)

            return redirect(url_for("index"))

    return render_template("index.html", form=form)


@app.route("/<table>", methods=["GET", "POST"])
def my_table(table):
    if session and "form_validated" in session and "table" in  session:
        if session["table"] == table:
            return render_template("table.html", table=session["table"])
        
        else:
            flash("Remplissez le formulaire pour avoir votre table")
            return redirect(url_for("index"))

    else:
        flash("Remplissez le formulaire pour avoir votre table")
        return redirect(url_for("index"))


@app.route("/suggestion/<full_name>/<table>", methods=["GET", "POST"])
def redirect_suggestion(full_name, table):
    #  flash('in')
     session["form_validated"] =True
     session["full_name"] = full_name
     session["table"] = table
     session['suggestion_lst'] = False

     return redirect(url_for("my_table", table=session["table"]))
