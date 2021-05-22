import random

import requests
from flask import Flask, render_template, request
#import requests_cache
from twilio.rest import Client
import random
#from werkzeug.utils import secure_filename
#import os
app = Flask(__name__, static_url_path='/static')
account_sid='AC7e73b300e4587f1dfd6555e100c9aa0b'
auth_token='7df96ba19e6c25bd42eb74304003a6f8'
client=Client(account_sid,auth_token)
UPLOAD_FOLDER="E:/temp"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
@app.route('/')
def form():
    return render_template('f1.html')


@app.route('/submit', methods=['post', 'get'])
def submit():
    fname = request.form['n1']
    lname=request.form['l1']
    email=request.form['email']
    sourceST=request.form['sst']
    sourceDT=request.form['sdt']
    destinationST=request.form['dst']
    destinationDT=request.form['ddt']
    phone=request.form['phn']
    #idp = request.files['idp']
    #filename = secure_filename(idp.filename)
    #idp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    idp=request.form['idp']
    dt=request.form['tdt']
    res=request.form['msg']
    dec=request.form['msg1']
    r = requests.get('https://api.covid19india.org/v4/data.json')
    jData = r.json()
    cnt = jData[destinationST]['districts'][destinationDT]['total']['confirmed']
    pop = jData[destinationST]['districts'][destinationDT]['meta']['population']
    per = (cnt / pop) * 100
    token="Not Issued"
    if (per < 30 and request.method == 'POST'):
        status = "confirmed"
        token=random.randint(600000,900000)
        client.messages.create(to='whatsapp:+919666398811',from_="whatsapp:+14155238886",body="Hi"+" "+fname+" "+lname+" "+"Your travel from "+sourceST+" "+sourceDT+" to "+destinationST+" "+destinationDT+" on "+dt+" is "+status+" "+"token number "+str(token))
    else:
        status = "rejected"
        client.messages.create(to="whatsapp:+919666398811",from_="whatsapp:+14155238886", body = "Hi" + " " + fname + " " + lname + " " + "Your travel from" + sourceST + " " + sourceDT + " to" + destinationST + " " + destinationDT + " on " + dt + " is " + status)
    return render_template('op.html', vart=token,var1=fname,var2=lname,var3=email,var4=sourceST,var5=sourceDT,var6=destinationST,var7=destinationDT,var8=phone,var9=idp,var10=res,var13=dec,var11=dt,var12=status)
if (__name__ == '__main__'):
    app.run(port = 5001, debug=True)
