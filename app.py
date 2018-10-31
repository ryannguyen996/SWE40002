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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from rq import Queue
from rq.job import Job
from worker import conn

csvformat = ['Student ID\tUnit Number\tComments\tSatisfaction']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
nltk.data.path.append('./nltk_data/')
q = Queue(connection=conn)
from models import Result


def assert_format(destination):
    if destination.lower().endswith('.tsv'):
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
            job = q.enqueue_call(func=classifier, args=(destination,), result_ttl='5m')
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
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r"\d", " ", text)
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
        teacher0 = joblib.load('classifiers/Teacher.pkl')
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
                        teacher_topic=int(teacher0.predict(comments).item(0)),
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

    os.remove(destination)


def scale(unscaledNum, minAllowed, maxAllowed, minCount, maxCount):
    return int(round((maxAllowed - minAllowed) * (unscaledNum - minCount) / (maxCount - minCount) + minAllowed))


#def color(number):
#    if(number == 0.0):
#        return "#ff0040"
#    if(number == 0.1):
#        return "#ff0000"
#    if(number == 0.2):
#        return "#ff4000"
#    if(number == 0.3):
#        return "#ff8000"
#    if(number == 0.4):
#        return "#ffbf00"
#    if(number == 0.5):
#        return "#ffff00"
#    if(number == 0.6):
#        return "#bfff00"
#    if(number == 0.7):
#        return "#80ff00"
#    if(number == 0.8):
#        return "#40ff00"
#    if(number == 0.9):
#        return "#00ff00"
#    if(number == 1.0):
#        return "#00ff40"
#    if(number > 1.0):
#        return "#ffff00"

# add 3 shade
def color(number):
    if(number == 0.0):
        return "#c40031"
    if(number == 0.1):
        return "#c40000"
    if(number == 0.2):
        return "#c43100"
    if(number == 0.3):
        return "#c46200"
    if(number == 0.4):
        return "#c49300"
    if(number == 0.5):
        return "#c4c400"
    if(number == 0.6):
        return "#93c400"
    if(number == 0.7):
        return "#62c400"
    if(number == 0.8):
        return "#31c400"
    if(number == 0.9):
        return "#00c400"
    if(number == 1.0):
        return "#00c431"
    if(number > 1.0):
        return "#c4c400"


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
            return "Upload successfully, Please wait for process.", 202
        else:
            return "Wrong csv format!", 202
    else:
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
    except:
        return "Error retriveing unit number and topic", 406

    topic = data["topic"]
    lists = []

    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic == 1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic == 1)
    if("teacher" in topic):
        a1 = a1.filter(Result.teacher_topic == 1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic == 1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic == 1)

    a1 = a1.all()

    if is_empty(a1):
        return "There is no comment satisfies the requirements", 406

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        teacher0 = joblib.load('classifiers/Teacher.pkl')
        class0 = joblib.load('classifiers/Class.pkl')
        assessment0 = joblib.load('classifiers/Assessment.pkl')
        resource0 = joblib.load('classifiers/Resource.pkl')
        other0 = joblib.load('classifiers/Other.pkl')

    for a2 in a1:
        temp = re.split('\band\b|,|\.', a2.comment, flags=re.IGNORECASE)
        temp1 = ""
        for a3 in temp:
            a4 = clean_text(str(a3))
            a4 = [a4]
            if("assessment" in topic):
                if(assessment0.predict(a4).item(0) == 1):
                    temp1 += a3
            elif("class" in topic):
                if(class0.predict(a4).item(0) == 1):
                    temp1 += a3
            elif("teacher" in topic):
                if(teacher0.predict(a4).item(0) == 1):
                    temp1 += a3
            elif("resource" in topic):
                if(resource0.predict(a4).item(0) == 1):
                    temp1 += a3
            elif("other" in topic):
                if(other0.predict(a4).item(0) == 1):
                    temp1 += a3
            else:
                temp1 += a3
        a2.comment = temp1

    for a2 in a1:
        a2.comment = clean_text(str(a2.comment))
        lists.append(a2.comment)

    tokens = []

    for a2 in lists:
        tokens = tokens + nltk.word_tokenize(a2)

    text = nltk.Text(tokens)

    c = Counter(text).most_common(30)
    print(c)

    jsonlist = []
#calulate size
    width = 400
    maxCount = c[0][1]
    minCount = c[len(c)-1][1]
    maxWordSize = width * 0.15
    minWordSize = maxWordSize / 5
    spread = maxCount - minCount
    if (spread <= 0):
        spread = 1
    step = (maxWordSize - minWordSize) / spread

    for i in c:
        e = 0
        for a2 in a1:
            if i[0] in a2.comment:
                e += a2.sentiment
        e = round((float(e)/i[1]), 1)
        dicta = {'text': i[0], 'size': round(maxWordSize - ((maxCount - i[1])*step)), 'color': color(e)}
        jsonlist.append(dicta)

    jsonStr = json.dumps(jsonlist)
    return jsonify(jsonStr), 200


@app.route('/getwordcloudcount', methods=['POST'])
def getwordcloudcount():
    # get url
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
    except:
        return " ", 406

    topic = data["topic"]
    lists = []
    lists1 = []

    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))
    a3 = a1

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic == 1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic == 1)
    if("teacher" in topic):
        a1 = a1.filter(Result.teacher_topic == 1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic == 1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic == 1)

    a1 = a1.all()
    a3 = a3.all()
    if is_empty(a1):
        return " ", 406

    for a2 in a1:
        lists.append(a2.comment)
    for a2 in a3:
        lists1.append(a2.comment)

    return ("There are {} out of {} comments satisfy the selection").format(str(len(lists)), str(len(lists1))), 200


@app.route('/getavg', methods=['POST'])
def getavg():
    # get url
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
    except:
        return " ", 406
    topic = data["topic"]

    a3 = 0
    a4 = 0
    a7 = 0
    a8 = 0
    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))
    a6 = a1

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic == 1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic == 1)
    if("teacher" in topic):
        a1 = a1.filter(Result.teacher_topic == 1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic == 1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic == 1)

    a1 = a1.all()
    a6 = a6.all()
    if is_empty(a1):
        return " ", 406

    for a2 in a6:
        a7 += a2.satisfaction
        a8 += 1

    for a2 in a1:
        a3 += a2.satisfaction
        a4 += 1

    a5 = a3/a4
    a9 = a7/a8
    print(a5)
    print(a9)
    return ("The average satisfaction score for the selection is {}/10.The average satisfaction score for this unit is {}/10").format(round(a5, 2), round(a9, 2)), 200
    #return ("The average sastisfaction score is {0:.2f} ").format(round(a5, 2)), 200


@app.route("/statistics", methods=['GET'])
def statistics():
    lists = []
    a1 = Result.query.with_entities(Result.unit_number).order_by(Result.unit_number).distinct()
    for a2 in a1:
        lists.append(a2.unit_number)
    return render_template('statistics.html', lists=lists)


@app.route("/getimage", methods=['POST'])
def getimage():
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
        graph = data["graph"]
    except:
        return " ", 406

    topic = data["topic"]
    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic == 1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic == 1)
    if("teacher" in topic):
        a1 = a1.filter(Result.teacher_topic == 1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic == 1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic == 1)

    df = pd.read_sql(a1.statement, a1.session.bind)
    graph = int(graph)
    if (graph == 1):
        df_clean = df.drop(columns=['id', 'student_id', 'unit_number', 'comment', 'satisfaction', 'sentiment'])
        counts = []
        categories = list(df_clean.columns.values)
        for i in categories:
            counts.append((i, df_clean[i].sum()))
        df_stats = pd.DataFrame(counts, columns=['category', 'number_of_comments'])
        df_stats['category'][0] = 'Assessment'
        df_stats['category'][1] = 'Class'
        df_stats['category'][2] = 'Teacher'
        df_stats['category'][3] = 'Resource'
        df_stats['category'][4] = 'Other'

        df_stats.plot(x='category', y='number_of_comments', kind='bar', legend=False, grid=False, figsize=(8, 5))
        plt.title("Number of comments per category")
        plt.ylabel('# of Comments', fontsize=12)
        plt.xlabel('category', fontsize=12)

    if (graph == 2):
        df_clean = df.drop(columns=['id', 'student_id', 'unit_number', 'comment', 'satisfaction', 'sentiment'])
        print(df_clean)
        rowsums = df_clean.iloc[:, 0:].sum(axis=1)
        x = rowsums.value_counts()
        plt.figure(figsize=(8, 5))
        sns.barplot(x.index, x.values)
        plt.title("Multiple categories per comment")
        plt.ylabel('# of Comments', fontsize=12)
        plt.xlabel('# of Categories', fontsize=12)

    if (graph == 3):
        lens = df.comment.str.len()
        print(lens)
        lens = lens.hist(grid=False, bins=np.arange(0, 1500, 100))
        lens.set_xlabel('Comments length (number of characters)')
        lens.set_ylabel('# of Comments')
        lens.set_title('Comment length distribution')

    if (graph == 4):
        df_clean = df['sentiment']
        count0 = df_clean.sum()
        print(count0)
        print(df_clean.count())
        labels = 'Positive', 'Negative'
        pos = (count0/df_clean.count())*100
        sizes = [pos, 100-pos]
        fig, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title('Sentiment distribution')

    if (graph == 5):
        df_clean = df['satisfaction']
        lens = df_clean.hist(grid=False, bins=np.arange(0, 10, 1))
        lens.set_xlabel('Score')
        lens.set_ylabel('# of Comments')
        lens.set_title('Satisfaction score distribution')

    fig = plt.gcf()
    fig.tight_layout()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    canvas.print_png(img)
    response = make_response(img.getvalue())
    response.mimetype = 'image/png'
    plt.close(fig)
    return response


@app.route("/downloadcsv", methods=['POST'])
def downloadcsv():
    data = json.loads(request.data.decode())

    try:
        unitnumber = data["unitnumber"]
    except:
        return " ", 406

    topic = data["topic"]
    a1 = Result.query
    a1 = a1.filter(Result.unit_number.in_(unitnumber))

    if("assessment" in topic):
        a1 = a1.filter(Result.assessment_topic == 1)
    if("class" in topic):
        a1 = a1.filter(Result.class_topic == 1)
    if("teacher" in topic):
        a1 = a1.filter(Result.teacher_topic == 1)
    if("resource" in topic):
        a1 = a1.filter(Result.resource_topic == 1)
    if("other" in topic):
        a1 = a1.filter(Result.other_topic == 1)

    df = pd.read_sql(a1.statement, a1.session.bind)
    df.drop(['id'], axis=1)
    resp = make_response(df.to_csv(index=False, sep='\t'))
    resp.headers["x-filename"] = "export.tsv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/help", methods=['GET'])
def help1():
    return render_template('help.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
