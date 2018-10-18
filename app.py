import os
import csv
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.externals import joblib
import numpy as np
import string
import re
import warnings
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO


csvformat = ['Student ID\tUnit Number\tComments\tSatisfaction']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
nltk.data.path.append('./nltk_data/')

from models import Result


def assert_format(destination):
    if destination.lower().endswith('.csv'):
        return True
    else:
        return False


def assert_csvformat(destination):
    with open(destination, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        i = reader.fieldnames
        print(csvformat)
        print(i)
        print(i == csvformat)
        if (i == csvformat):
            classifier(destination)
            return True
        else:
            return False


def clean_text(text):
    # Remove puncuation
    text = text.translate(string.punctuation)

    # Convert words to lower case and split them
    text = text.lower().split()

    # Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if w not in stops and len(w) >= 3]

    text = " ".join(text)
    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r">", " ", text)
    text = re.sub(r"<", " ", text)
    text = re.sub(r"!", " ", text)
    text = re.sub(r":", " ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ", text)
    text = re.sub(r"\+", " ", text)
    text = re.sub(r"\-", " ", text)
    text = re.sub(r"\=", " ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    # Stemming
    text = text.split()
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(lemmatized_words)
    return text


def classifier(destination):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        lecture0 = joblib.load('classifiers/Lecture.pkl')
        class0 = joblib.load('classifiers/Class.pkl')
        assessment0 = joblib.load('classifiers/Assessment.pkl')
        resource0 = joblib.load('classifiers/Resource.pkl')
        other0 = joblib.load('classifiers/Other.pkl')
        sentiment0 = joblib.load('classifiers/SGDClassifier.pkl')

    with open(destination, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'YAY LOADED!')
                line_count += 1
            else:
                comments = clean_text(str({row[2]}))
                comments = [comments]
                line_count += 1
                try:
                    result = Result(
                        student_id=int(row[0]),
                        unit_number=str(row[1]),
                        comment=str(row[2]),
                        satisfaction=int(row[3]),
                        assessment_topic=int(assessment0.predict(comments).item(0)),
                        class_topic=int(class0.predict(comments).item(0)),
                        lecture_topic=int(lecture0.predict(comments).item(0)),
                        other_topic=int(other0.predict(comments).item(0)),
                        resource_topic=int(resource0.predict(comments).item(0)),
                        sentiment=int(sentiment0.predict(comments).item(0))
                    )
                    db.session.add(result)
                    db.session.commit()
                    print(result.id)
                except:
                    print(f'ERROR')
            print(f'Processed {line_count} lines.')


def scale(unscaledNum, minAllowed, maxAllowed, minCount, maxCount):
    return int(round((maxAllowed - minAllowed) * (unscaledNum - minCount) / (maxCount - minCount) + minAllowed))


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/upload", methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route("/uploads", methods=['POST'])
def uploads():
    # See more http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
    upload = request.files['file']
    print('Received file', upload.filename)
    target = os.path.join(APP_ROOT, 'files')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    if(assert_format(destination)):
        if(assert_csvformat(destination)):
            os.remove(destination)
            return "YAY! Process to wordcloud generator page", 202
        else:
            os.remove(destination)
            return "Wrong csv format!", 202
    else:
        os.remove(destination)
        return "Wrong file type!", 202


@app.route("/wordcloud", methods=['GET'])
def wordcloud():
    lists = []
    a1 = Result.query.with_entities(Result.unit_number).order_by(Result.unit_number).distinct()
    for a2 in a1:
        lists.append(a2.unit_number)
    return render_template('wordcloud.html', lists=lists)


@app.route('/getwordcloud', methods=['POST'])
def getwordcloud():
    # get url
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
        topic = data["topic"]
        print(topic)
    except:
        return "Error retriveing unit number and topic", 406

    lists = []

    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic==1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic==1)
    if("lecture" in topic):
        a1 = a1.filter(Result.lecture_topic==1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic==1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic==1)

    a1 = a1.all()

    if is_empty(a1):
        return "There is no comment satisfies the requirements", 406

    for a2 in a1:
        lists.append(a2.comment)

    tokens = []

    for a2 in lists:
        a2 = clean_text(str(a2))
        tokens = tokens + nltk.word_tokenize(a2)

    text = nltk.Text(tokens)
    c = Counter(text).most_common(30)
    print(c)

    try:
        jsonlist = []
        b = 1
        for i in c:
            dicta = {'id' :b ,'word' :i[0] ,'size': scale(i[1], 1, 10, c[len(c)-1][1], c[0][1])}
            b += 1
            jsonlist.append(dicta)
        jsonStr = json.dumps(jsonlist)
    except:
        print("Something's wrong")
        return "Internal server error", 500

    return jsonify(jsonStr), 200

@app.route('/getwordcloudcount', methods=['POST'])
def getwordcloudcount():
    # get url
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
        topic = data["topic"]
    except:
        return " ", 406

    lists = []

    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic==1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic==1)
    if("lecture" in topic):
        a1 = a1.filter(Result.lecture_topic==1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic==1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic==1)

    a1 = a1.all()
    if is_empty(a1):
        return " ", 406

    for a2 in a1:
        lists.append(a2.comment)

    return ("There are {} comments satisfy the selection" ).format(str(len(lists))),200

@app.route('/getavg', methods=['POST'])
def getavg():
    # get url
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
        topic = data["topic"]
    except:
        return " ", 406

    a3 = 0
    a4 = 0
    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic==1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic==1)
    if("lecture" in topic):
        a1 = a1.filter(Result.lecture_topic==1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic==1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic==1)

    a1 = a1.all()
    if is_empty(a1):
        return " ", 406

    for a2 in a1:
        a3 += a2.satisfaction
        a4 += 1

    a5 = a3/a4
    print(a5)
    return ("The average sastisfaction score is {0:.2f} " ).format(round(a5,2)),200

@app.route("/statistics", methods=['GET'])
def statistics():
    #lists = []
    #a1 = Result.query.with_entities(Result.unit_number).order_by(Result.unit_number).distinct()
    #for a2 in a1:
    #    lists.append(a2.unit_number)
    #return render_template('statistics.html', lists=lists)
    return render_template('uc.html')

@app.route("/getimage", methods=['GET'])
def getimage():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
