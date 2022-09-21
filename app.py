import flask
application = flask.Flask(__name__)
@application.route("/")
def root():
  return "Hello World!"

if __name__ == "__main__":
  application.run("0.0.0.0", 80)
