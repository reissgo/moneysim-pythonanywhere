# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, url_for, render_template, request

#import matplotlib.pyplot as plt

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
    #plt.cla()
    #plt.clf()
    #plt.plot([0,xx],[0,yy])
    #plt.savefig('static/'+fname)
    return render_template("index.htm", thestring=fname, defx=xx, defy=yy)

if __name__ == "__main__":
    app.run(debug=True)
