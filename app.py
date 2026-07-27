from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "library123"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "library"

mysql = MySQL(app)

#  HOME 
@app.route("/")
def home():
    return render_template("login.html")


#  LOGIN 
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cur.fetchone()

    cur.close()

    if user:
        session["admin"] = username
        return redirect("/dashboard")

    return render_template("login.html",
                           message="Invalid Username or Password")


# DASHBOARD 
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/")

    return render_template("dashboard.html")


#  ADD BOOK 
@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        book_name = request.form["book_name"]
        author = request.form["author"]
        publication = request.form["publication"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO books
            (book_name, author, publication, category, quantity, available)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (book_name,
              author,
              publication,
              category,
              quantity,
              quantity))

        mysql.connection.commit()

        cur.close()

        return redirect("/add_book")

    return render_template("add_book.html")


#  LOGOUT 
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


#  RUN 
if __name__ == "__main__":
    app.run(debug=True)