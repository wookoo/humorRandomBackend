from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
import requests
from bs4 import BeautifulSoup
import datetime

def user(request):

    try:



        try:
            year = request.GET['year']
            month = request.GET['month']
            day = request.GET['day']
            hour = request.GET['hour']
            min = request.GET['min']
            now = datetime.datetime.strptime(year+month+day+hour+min,"%Y%m%d%H%M")
        except:
            now = datetime.datetime.now()


        url = request.GET['url']

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

        r = requests.get(url,headers=headers)
        r.encoding = 'euc-kr'
        result = r.text
        soup = BeautifulSoup(result,"html.parser")
        writter = soup.find_all("td",{"class","info"})[1].find("span",{"class":"hu_nick_txt"}).text
        comments = soup.find('div',{'id':'wrap_cmt_new'})
        comments = comments.find_all('tr')
        result = {}
        result["status"] = "ok"
        result["writter"] = writter
        comments_writter = {}
        for i in comments:
            try:
                comment_writter = i.find('span',{'class':'hu_nick_txt'}).text
                comment_time = i.find('span',{'class':'list_date'}).text.strip()

                if comment_writter != writter and not comment_writter in comments_writter:
                    comments_writter[comment_writter] = comment_time

            except Exception as ex:
                pass

        result['comments'] = [i for i in comments_writter.keys() if datetime.datetime.strptime(comments_writter[i],"%Y-%m-%d %H:%M:%S") < now]
        return JsonResponse(result)

    except:
        return JsonResponse({"status":"error"})
