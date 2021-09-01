from tkinter import *
from tkinter.messagebox import *
import requests
from tkinter.scrolledtext import *
import requests
import json
import datetime
from newspaper import Article
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
#-----------------------------data preprocessing-----------------#
df = pd.read_csv('train.csv')
conversion_dict = {0:'Real',1:'Fake'}
df['label'] = df['label'].replace(conversion_dict)

day = str(datetime.datetime.now())
datetime_values = day.split()
today = datetime_values[0]
searchedArticles = []
#---------------------------------------------------#
#Model creation
x_train , x_test ,y_train, y_test = train_test_split(df['text'], df['label'], test_size = 0.25, random_state=7, shuffle = True)
tfidf_vectorizer = TfidfVectorizer(stop_words='english',max_df=0.7)

vec_train = tfidf_vectorizer.fit_transform(x_train.values.astype('U'))
vec_test = tfidf_vectorizer.transform(x_test.values.astype('U'))

pac = PassiveAggressiveClassifier(max_iter = 50)
pac.fit(vec_train,y_train)

y_pred = pac.predict(vec_test)
score = accuracy_score(y_test, y_pred)
#--------------------------------Functions-----------------------------#
def display(n):
    if n==1:
        hdlines_window.deiconify()
        mainwindow.withdraw()
        getHeadlines()
    elif n==2:
        rd_news_window.deiconify()
        mainwindow.withdraw()
    elif n==3:
        chk_window.deiconify()
        clear()
        mainwindow.withdraw()
    elif n==4:
        srch_news_window.deiconify()
        mainwindow.withdraw()
def back(n):
    if n==1:
        mainwindow.deiconify()
        hdlines_window.withdraw()
    elif n==2:
        mainwindow.deiconify()
        text_area_rd.configure(state='normal')
        text_area_rd.delete(1.0,END)
        text_area_rd.configure(state='disabled')
        keyword_ent_rd.delete(0,END)
        rd_news_window.withdraw()
    elif n==3:
        mainwindow.deiconify()
        chk_window.withdraw()
    elif n==4:
        mainwindow.deiconify()
        srch_news_window.withdraw()

#-------------------------Main Window ---------------------------------#
mainwindow = Tk()
mainwindow.title("Fake News App")
mainwindow.geometry("900x500+500+10")
mainwindow.resizable(0,0)
f=('Calibri',25,'bold')

window_title = Label(mainwindow,text="Detecting Fake News",font=('calibri',40,'bold'),fg="white",bg="steelblue",width="900")
window_title.pack(pady=10)

headlines_btn = Button(mainwindow,text="Headlines",font=f,width=20,bg="red",fg="White",relief="raised",bd=5,command=lambda:display(1))
headlines_btn.place(x=50,y=150)

readnews_btn = Button(mainwindow,text="Read News",font=f,width=20,bg="red",fg="White",relief="raised",bd=5,command=lambda:display(2))
readnews_btn.place(x=450,y=150)

verifynews_btn = Button(mainwindow,text="Verify News",font=f,width=20,bg="red",fg="White",relief="raised",bd=5,command=lambda:display(3))
verifynews_btn.place(x=50,y=350)

searchnews_btn = Button(mainwindow,text="Search News",font=f,width=20,bg="red",fg="White",relief="raised",bd=5,command=lambda:display(4))
searchnews_btn.place(x=450,y=350)

#-----------------------------Check news---------------------------------#
def clear():
    article.delete(1.0,END)
def chk_news():
    data = article.get(1.0,END)
    vec_newtest = tfidf_vectorizer.transform([data])
    y_predl = pac.predict(vec_newtest)
    # return y_predl[0]
    if y_predl[0] == 'Real':
        showinfo("Result","News article is Genuine")
    elif y_predl[0] == 'Fake':
        showinfo("Result","News article is Fake")

chk_window = Toplevel(mainwindow)
chk_window.title("Verify fake News")
chk_window.geometry("600x750+500+10")
chk_window.resizable(0,0)

window_title = Label(chk_window,text="Detecting Fake News",font=('calibri',40,'bold'),fg="white",bg="steelblue",width="900")
window_title.pack(pady=10)

enter_txt_label = Label(chk_window, text = "Enter news article below.",font=f)
enter_txt_label.place(x=30,y=100)

article = Text(chk_window,bd=5,font = f)
article.place(x=40,y=150,width = 500 , height=400 )

chk_btn = Button(chk_window,text="VERIFY",font=f,width=10,bg="red",fg="White",relief="raised",bd=5,command=chk_news)
chk_btn.place(x=100,y=580)

chk_clr_btn = Button(chk_window,text="CLEAR",font=f,width=10,bg="red",fg="White",relief="raised",bd=5,command=clear)
chk_clr_btn.place(x=300,y=580)

chk_back_btn = Button(chk_window,text="Back",font=f,width=22,bg="orange",fg="white",relief="raised",bd=5,command=lambda:back(3))
chk_back_btn.place(x=100,y=670)
#-----------------------------Headlines--------------------------#
def getHeadlines():
    url = "https://newsapi.org/v2/everything?sources=the-hindu&apiKey=2d084c33993546cc9ad27a69c4f0905a"
    response = requests.get(url)
    content = json.loads(response.content)
    text_area.delete(1.0,END)
    count =1
    temp =""
    line = ""
    for i in content['articles']:
        article ={}
        hd = i['title']
        temp = str(count)+"]  "
        text_area.insert(INSERT, temp,"ptr")
        line = str(hd)+"\n\n" 
        text_area.insert(INSERT,line) 
        count +=1   
        article['title'] = i['title']
        article['url'] = i['url']
        searchedArticles.append(article)
    text_area.tag_config("ptr",foreground="steelblue")
    text_area.configure(state='disabled')   


hdlines_window = Toplevel(mainwindow)
hdlines_window.title("Headlines")
hdlines_window.geometry("900x800+500+10")
hdlines_window.resizable(0,0)
window_title = Label(hdlines_window,text=" Top Headlines",font=('calibri',40,'bold'),fg="white",bg="steelblue",width="900")
window_title.pack(pady=10)

text_area = ScrolledText(hdlines_window, width = 700, height = 20,font = ("Times New Roman",18))
text_area.pack(pady=10)

back_btn = Button(hdlines_window,text="Back",font=f,width=24,bg="orange",fg="white",relief="raised",bd=5,command=lambda:back(1))
back_btn.pack()
#-----------------------------search news--------------------------#
def searchNews():
    text_area_srch.configure(state='normal')  
    text_area_srch.delete(1.0,END)
    search = str(keyword_ent.get())
    url = "https://newsapi.org/v2/everything/?q="+search+"&from="+"today"+"&sortBy=popularity&apiKey=2d084c33993546cc9ad27a69c4f0905a"

    response = requests.get(url)
    content = json.loads(response.content)
    
    count =1
    temp =""
    line = ""
    for i in content['articles']:
        article={}
        hd = i['title']
        temp = str(count)+"]  "
        text_area_srch.insert(INSERT, temp,"ptr")
        line = str(hd)+"\n\n" 
        text_area_srch.insert(INSERT,line) 
        count +=1   
        article['title'] =  i['title']
        article['url'] = i['url']
        searchedArticles.append(article)
    text_area_srch.tag_config("ptr",foreground="steelblue")
    text_area_srch.configure(state='disabled')   


srch_news_window = Toplevel(mainwindow)
srch_news_window.title("Search News")
srch_news_window.geometry("900x800+500+10")
srch_news_window.resizable(0,0)
window_title = Label(srch_news_window,text="Search News",font=('calibri',40,'bold'),fg="white",bg="steelblue",width="900")
window_title.pack(pady=10)

keyword_lbl = Label(srch_news_window,text="Enter Keyword",font=f)
keyword_lbl.place(x=30,y=100)

keyword_ent = Entry(srch_news_window,bd=4,font=f,width=50,fg="steelblue")
keyword_ent.place(x=30,y=150)

header_lbl = Label(srch_news_window,text="Headlines for your search",font=f,bg="orange",fg="white",width=55)
header_lbl.place(x=0,y=205)

text_area_srch = ScrolledText(srch_news_window, width = 70, height = 16,font = ("Times New Roman",18))
text_area_srch.place(x=15,y=260)

back_btn = Button(srch_news_window,text="Back",font=f,width=15,bg="red",fg="white",relief="raised",bd=5,command=lambda:back(4))
back_btn.place(x=520,y=705)

srch_btn = Button(srch_news_window,text="Search",font=f,width=15,bg="red",fg="white",relief="raised",bd=5,command=searchNews)
srch_btn.place(x=150,y=705)

#-----------------------------Read news--------------------------#
def getNews():
    text_area_rd.configure(state='normal')  
    text_area_rd.delete(1.0,END)
    search = str(keyword_ent_rd.get())

    for item in searchedArticles:
        if search == item['title']:
            s_url = item['url'] 
            news_article = Article(s_url,language='en')
            news_article.download()
            news_article.parse()
            block =news_article.text
            text_area_rd.insert(INSERT,block) 
    text_area_rd.tag_config("ptr",foreground="steelblue")
    text_area_rd.configure(state='disabled')   


rd_news_window = Toplevel(mainwindow)
rd_news_window.title("Read News")
rd_news_window.geometry("900x800+500+10")
rd_news_window.resizable(0,0)
window_title = Label(rd_news_window,text="Read News Article",font=('calibri',40,'bold'),fg="white",bg="steelblue",width="900")
window_title.pack(pady=10)

keyword_lbl = Label(rd_news_window,text="Enter headline",font=f)
keyword_lbl.place(x=30,y=100)

keyword_ent_rd = Entry(rd_news_window,bd=4,font=f,width=50,fg="steelblue")
keyword_ent_rd.place(x=30,y=150)

header_lbl = Label(rd_news_window,text="Arctile for your search",font=f,bg="orange",fg="white",width=55)
header_lbl.place(x=0,y=205)

text_area_rd = ScrolledText(rd_news_window, width = 70, height = 16,font = ("Times New Roman",18))
text_area_rd.place(x=15,y=260)

back_btn = Button(rd_news_window,text="Back",font=f,width=15,bg="red",fg="white",relief="raised",bd=5,command=lambda:back(2))
back_btn.place(x=520,y=705)

srch_btn = Button(rd_news_window,text="Search",font=f,width=15,bg="red",fg="white",relief="raised",bd=5,command=getNews)
srch_btn.place(x=150,y=705)
print(searchedArticles)

chk_window.withdraw()
hdlines_window.withdraw()
srch_news_window.withdraw()
rd_news_window.withdraw()
mainwindow.mainloop()