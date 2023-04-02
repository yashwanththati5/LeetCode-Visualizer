from flask import Flask, request, render_template 
import requests
from bs4 import BeautifulSoup 
def extract(y):
     s = ""
     for i in range(95 , len(y)):
          if y[i].isdigit():
               s += y[i]
          elif y[i] == '<':
               break
     return s
app = Flask(__name__, template_folder='templates', static_folder='staticfiles') 
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/goback" , methods = ["POST"])
def goback():
     return render_template('index.html')
@app.route("/check" , methods = ["POST"])
def check():
    name = request.form.get('name')
    string = "https://leetcode.com/"
    string = string + name
    html_text = requests.get(string).text
    soup = BeautifulSoup(html_text , 'lxml')
    data = []
    data.append(name)
    try:
        solved_count = soup.find("div" , class_ = "text-[24px] font-medium text-label-1 dark:text-dark-label-1").text
        contest_count = soup.find("div" , class_ = "hidden md:block").text
        contest_rating = soup.find("div" , class_ = "text-label-1 dark:text-dark-label-1 flex items-center text-2xl").text
        data.append(solved_count)
        data.append(contest_count[8:])
        data.append(contest_rating)
        x = soup.find_all("span" , class_ = "mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1")
        for item in x:
             data.append(extract(str(item)))
        try:
              github_link = soup.find_all("a" , class_= "hover:text-label-1 dark:hover:text-dark-label-1 cursor-pointer").text
              data.append(github_link)
        except:
             print()
        # print(f' UserId: {getusr} \n Solved Count: {solved_count} \n Contests Attended: {contest_count[8:]} \n Rating: {contest_rating}')
    except:
        return render_template('failure.html')
    return render_template('sucees.html' , data = data)
if __name__ =='__main__':  
    app.run()  