from flask import Flask, render_template, request
from RecommendationFile import *

app = Flask(__name__)
app.debug = False  # When Debug is True, it computes the SVD, False just load from files


@app.route("/")
def main():
    # noinspection PyUnresolvedReferences
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    if app.debug:
        recommend('ml-100k/u.data')  # Change data set here

    recommendation_file = np.load("rec_results-100k.dat")
    user = int(request.form['text'])
    rc = recommendation_file[user]
    # noinspection PyUnresolvedReferences
    return render_template('recommend.html', recs=rc)


if __name__ == "__main__":
    app.run()
