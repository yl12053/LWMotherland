import flask
app = flask.Flask(__name__)
@app.route("/")
def root():
  return "Hello World!"

if __name__ == "__main__":
  app.run("0.0.0.0", 80)
