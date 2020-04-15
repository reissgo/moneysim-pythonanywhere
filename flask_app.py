from flask import Flask, render_template, request
import sys
import os
import time

import matplotlib.pyplot as plt
import matplotlib
import copy

global_formlist = []

app = Flask(__name__)
user_counter = 1
post_ctr = 0
get_ctr = 0
pg_hist="Start:"

id_read_from_form=1
has_been_executed="not yet"
diagnostic_string="...  "

class FormItemStartSetup:
    def __init__(self, text, thetype, form_var, value, minv, maxv):

        # these are fixed forever
        self.text_to_display = text
        self.form_var = form_var
        self.type = thetype # int / float / flag
        self.start_value = value
        self.minv = minv
        self.maxv = maxv

        self.user_error_message = ""
        self.user_error_flag = False
        self.user_value = value

def idx_of_form_var(fv):
    for i, fi in enumerate(global_formlist):
        if fi.form_var == fv:
            return i
    return -99

def user_value_of_form_var(fv,fl):
    return fl[idx_of_form_var(fv)].user_value


@app.route("/", methods=["POST", "GET"])
def home():
    global user_counter,has_been_executed,id_read_from_form,diagnostic_string,post_ctr,get_ctr, pg_hist, global_formlist
    formlist = copy.deepcopy(global_formlist)
    diagnostic_string = ""
    id_read_from_form = -1

    if request.method == 'POST':
        for fi in formlist:
            try:
                fi.user_value = request.form[fi.form_var]
            except:
                fi.user_value= "???"

            if fi.type == "float":
                try:
                    float(fi.user_value)
                except:
                    fi.user_error_message = "Bad float"
            elif fi.type == "int":
                try:
                    int(fi.user_value)
                except:
                    fi.user_error_message = "Bad integer"

            if fi.type == "int" and fi.user_error_message == "" and fi.minv != "":
                if int(fi.user_value) < int(fi.minv):
                    fi.user_error_message = "Must be at least "+fi.minv
            if fi.type == "int" and fi.user_error_message == "" and fi.maxv != "":
                if int(fi.user_value) > int(fi.maxv):
                    fi.user_error_message = "Must be at most "+fi.maxv
            if fi.type == "float" and fi.user_error_message == "" and fi.minv != "":
                if float(fi.user_value) < float(fi.minv):
                    fi.user_error_message = "Must be at least "+fi.minv
            if fi.type == "float" and fi.user_error_message == "" and fi.maxv != "":
                if float(fi.user_value) > float(fi.maxv):
                    fi.user_error_message = "Must be at most "+fi.maxv

        if int(user_value_of_form_var("npc",formlist)) > int(user_value_of_form_var("nag",formlist)):
            formlist[idx_of_form_var("npc")].user_error_message = "'"+formlist[idx_of_form_var("npc")].text_to_display+"' must be less than '"+formlist[idx_of_form_var("nag")].text_to_display+"'"
            formlist[idx_of_form_var("nag")].user_error_message = "'"+formlist[idx_of_form_var("npc")].text_to_display+"' must be less than '"+formlist[idx_of_form_var("nag")].text_to_display+"'"

        id_read_from_form = str(request.form['custId'])

    user_counter += 1
    fname = "test"+str(id_read_from_form)+"_"+str(formlist[idx_of_form_var("form_x")].user_value)+"_"+str(formlist[idx_of_form_var("form_y")].user_value)+".png"
    plt.cla()
    plt.clf()
    plt.plot([0,float(user_value_of_form_var("form_x",formlist))],[0,float(user_value_of_form_var("form_y",formlist))])
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

    #if user_seen_before(id_read_from_form):
    #else:


    if id_read_from_form == -1:
        id_for_hidden_thing = user_counter
    else:
        id_for_hidden_thing = id_read_from_form

    return render_template("index.htm",
        thestring='/static/'+fname,

        defid=id_for_hidden_thing,
        params1="",#url_for('/mysite/static'),
        params2="Python version "+sys.version,
        params3="Matplotlib version "+matplotlib.__version__,
        params4="os.getcwd() is "+os.getcwd(),
        params5=str(user_counter),
        params6=diagnostic_string,
        fl=formlist,
        post_c=post_ctr,
        get_c=get_ctr,
        pg_hist=pg_hist
        )

global_formlist.append(FormItemStartSetup(                                        "x","int",      "form_x",    "10", "",""))
global_formlist.append(FormItemStartSetup(                                        "y","int",      "form_y",    "20", "",""))
global_formlist.append(FormItemStartSetup(                         "Number of agents","int",         "nag",    "30", "2","100"))
global_formlist.append(FormItemStartSetup(                   "Typical starting money","float",       "tsm", "100.0", ".001","1000000"))
global_formlist.append(FormItemStartSetup(          "Num agents for price comparison","int",         "npc",     "3", "1","100"))
global_formlist.append(FormItemStartSetup(               "Typical goods made per day","float",      "tgpd",  "10.0", ".001","100"))
global_formlist.append(FormItemStartSetup(                    "Num iterations to run","int",         "nir","150000", "1","1000000"))
global_formlist.append(FormItemStartSetup(                                "Max stock","float",     "maxst",  "70.0", "1",""))
global_formlist.append(FormItemStartSetup(       "Typical days between price changes","float",      "tdpc",   "3.0", ".1","100"))
global_formlist.append(FormItemStartSetup(           "Typical days between purchases","float",      "tdbp",   "1.0", ".1","100"))
global_formlist.append(FormItemStartSetup(                   "Typical starting price","float",       "tsp",   "2.0", ".00001",""))



if __name__ == "__main__":
    app.run(debug=True)
