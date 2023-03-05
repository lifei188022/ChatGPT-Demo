from flask import Flask, render_template, request
from flask import Flask,jsonify,render_template,render_template_string,request,redirect, url_for, make_response,session
import openai
import os
import requests,json,time
from datetime import timedelta,datetime

openai.api_key = '' # 输入自己的api_key
assert(openai.api_key)
app = Flask(__name__)
app.secret_key='QWERTYUIOP'
@app.route('/')
def index():
    return render_template("login.html")
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('pwd')
    if username == "zhaobo" and password == "zhaobo":
        session['user_info']=username
        return redirect('/home')
        #return render_template("test1.html", msg="登录成功")
    else:
        return render_template("login.html", msg="登录失败")

messages = []
@app.route('/home')
def home():
    user_info=session.get('user_info')
    if not user_info:
        return redirect('/')
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])

def get_bot_response():
    message = request.form['message']
    # print(user_input)
    messages.append({'role': 'user', 'content': message})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = completion.choices[0].message['content']
    print(response)
    # messages.append({'role': 'assistant', 'content': response})
    # print(messages)
    with open('jilu.txt', mode='a', encoding='utf8') as f:
        f.writelines(str(datetime.now()+timedelta(hours=8))+'\n')
        f.writelines(message+'\n')
        f.writelines(response.strip()+'\n')
        f.close()
    return response

if __name__ == '__main__':
    app.run("0.0.0.0",port=80,debug=True)
