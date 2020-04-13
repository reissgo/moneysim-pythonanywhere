# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, url_for, render_template, request
import sys
import os

import matplotlib.pyplot as plt
import matplotlib

app = Flask(__name__)
xx=5
yy=7
@app.route("/", methods=["POST", "GET"])
def home():
    global xx,yy

    if request.method == 'POST':
        xx = float(request.form['form_x'])
        yy = float(request.form['form_y'])

    fname = "test"+str(xx)+"_"+str(yy)+".png"
    plt.cla()
    plt.clf()
    plt.plot([0,xx],[0,yy])
    plt.savefig('mysite/static/'+fname)
    return render_template("index.htm",
        thestring='/static/'+fname,
        defx=xx,
        defy=yy,
        params1="",#url_for('/mysite/static'),
        params2="Python version "+sys.version,
        params3="Matplotlib version "+matplotlib.__version__,
        params4="os.getcwd() is "+os.getcwd(),
        params5="5 not set",
        params6="6 not set"
        )

if __name__ == "__main__":
    app.run(debug=True)
