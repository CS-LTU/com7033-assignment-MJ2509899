from flask import Flask, render_template, request

app = Flask(__name__)

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Example: simple form input processing
        name = request.form.get("name")
        age = request.form.get("age")
        result = f"Hello {name}! You are {age} years old."
    return render_template("index.html", result=result)

# About page
@app.route("/about")
def about():
    return render_template("result.html", message="This is a simple Flask web server example!")

if __name__ == "__main__":
    app.run(debug=True)
