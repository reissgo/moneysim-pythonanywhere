# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, url_for, render_template, request
import sys
import os
import time

import matplotlib.pyplot as plt
import matplotlib

app = Flask(__name__)
user_counter = 1
xx=5
yy=7
id_read_from_form=1
has_been_executed="not yet"
diagnostic_string="...  "

@app.route("/", methods=["POST", "GET"])
def home():
    global xx,yy,user_counter,has_been_executed,id_read_from_form,diagnostic_string
    diagnostic_string = ""

    if request.method == 'POST':
        xx = float(request.form['form_x'])
        yy = float(request.form['form_y'])
        id_read_from_form = str(request.form['custId'])

    user_counter += 1
    fname = "test"+str(id_read_from_form)+"_"+str(xx)+"_"+str(yy)+".png"
    plt.cla()
    plt.clf()
    plt.plot([0,xx],[0,yy])
    plt.savefig('mysite/static/'+fname)

    now = time.time()
    file_list = os.listdir("mysite/static/")
    for f in file_list:
        if f.find(".png") >= 0:
            age = int(now-os.path.getmtime("mysite/static/"+f))
            diagnostic_string += ("["+f+"]["+str(age)+"]  ")
            if age > (60*60):
                os.remove("mysite/static/"+f)
        else:
            diagnostic_string += ("["+f+"]["+"NOT-A-PNG!!"+"]  ")

    return render_template("index.htm",
        thestring='/static/'+fname,
        defx=xx,
        defy=yy,
        defid=user_counter,
        params1="",#url_for('/mysite/static'),
        params2="Python version "+sys.version,
        params3="Matplotlib version "+matplotlib.__version__,
        params4="os.getcwd() is "+os.getcwd(),
        params5=str(user_counter),
        params6=diagnostic_string
        )

if __name__ == "__main__":
    app.run(debug=True)
