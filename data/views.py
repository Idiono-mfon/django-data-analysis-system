import tweepy
import pandas as pd
from textblob import TextBlob #for doing sentiment analysis
import numpy as np
import re #for cleaning text
import matplotlib.pyplot as plt
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Data,Comment
from account.models import CustomUser
from data.analytics import analyseData,clean,ratio,generateData
# for url encoding
import urllib.parse
import os
from django.conf import settings
from django.http import HttpResponse, Http404
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# this was added to imported the form created before
# from account.forms import DocumentForm
# for validation
from data.validator import validate_file_extension

# display validation messages
from django.contrib import messages

def getdataFile(data_id):
    dataUploaded = Data.objects.get(pk = data_id)
    path = dataUploaded.path
    # /media/nnpower_ng.csv
    dir = 'c:/users/hp/projects/Empanalyst{}'
    df = pd.read_csv(dir.format(path))
    polarity = lambda x: TextBlob(x).sentiment.polarity
    subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
    df['polarity'] = df['tweet'].apply(polarity)
    df['subjectivity'] = df['tweet'].apply(subjectivity)
    df['analysis'] = df['polarity'].apply(ratio)

    return df

def computeNewDataframe(original_df,rows):
    datarow = []
    for i in range(rows):
        datarow.append(i)
    # datarow is an array holding the size of this series which will latter be the id of the entire dataframes
    # analy variable holds the analysis data
    analy = original_df.analysis
    # convert the analysis result to numpy array inorder to create a dataframe of id and analysis
    analy_array =   analy.to_numpy()
    # get the tweet series here
    tweetseries = original_df.tweet
    # convert the series to array here
    tweetarray = tweetseries.to_numpy()

    dateseries = original_df.time
    datearray = dateseries.to_numpy()
    # # create dataframe with tweetarray, analy_array, datarow(this is id array)
    # data_analy = pd.DataFrame({'id':datarow, 'analysis':analy_array,'tweet':tweetarray}, columns=['id','analysis','tweet'])
    # # merger the dataframe with the main comment dataframe
    # print(data_analy.tweet[1])
    # comments_m = pd.merge(tweets, data_analy, on='analysis')
    # tweet = pd.merge(tweets,data_analy, left_on='analysis',right_on='analysis')
    result = {'id':datarow,'tweets':tweetarray,'date':datearray}

    return result


def comments (request):
    messages.info(request,"Upload Data First before comment can be generated")
    return redirect("analyse")



# Create your views here.
def Negativecomments(request, data_id):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    df = getdataFile(data_id)
    # get a dataframe of tweets where analysis == -1
    tweets = df.loc[df.analysis == -1, ['tweet','time','analysis']]
    # rows is the rows containing the number of rows
    rows,cols = tweets.shape
    # this will be row array
    result = computeNewDataframe(tweets,rows)
    return render(request, 'comments.html', {'name':username,'comment':True,'result': result})

def Positivecomments(request, data_id):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    df = getdataFile(data_id)
    # get a dataframe of tweets where analysis == -1
    tweets = df.loc[df.analysis == 1, ['tweet','time','analysis']]
    # rows is the rows containing the number of rows
    rows,cols = tweets.shape
    # this will be row array
    result = computeNewDataframe(tweets,rows)
    return render(request, 'comments.html', {'name':username,'comment':True,'result': result})

def Allcomments(request, data_id):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    df = getdataFile(data_id)
    # get a dataframe of tweets where analysis == -1
    # rows is the rows containing the number of rows
    rows,cols = df.shape
    # this will be row array
    result = computeNewDataframe(df,rows)
    return render(request, 'comments.html', {'name':username,'comment':True,'result': result})

def index (request):
    return render(request, 'index.html')

def success(request,data_id):
    if not request.user.is_authenticated:
        return redirect('login')
        data_id = data_id
    return render(request, 'trash.html',{'data_id':data_id})


def download(request, path):
    file_path = os.path.join(BASE_DIR, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def generate(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # put validation here latter
        name = request.POST['name']
        keyword = '@'+ request.POST['keyword']
        df = generateData(keyword,clean)
        path = 'uploads/'+ keyword +'.csv'
        response = download(request, path)
        return response
    else:
        # get the username of the authenticated user
        username = request.user.username
        return render(request,'scrape.html',{'name':username,'generate':True})  

  
def analyse (request):
        # this is for not uploading the file to the server
       
        # return render(request, 'analyse.html',{'uploaded_file_url': uploaded_file_url})
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        data = request.FILES.get('data',False)
        # validate file extension before saving
        statusDict = validate_file_extension(data,redirect,request)
        if statusDict["state"]:
            messages.info(request,statusDict["message"])
            return redirect("analyse")
        name = data.name
        fs = FileSystemStorage()
        filename = fs.save(data.name, data)
        # uploaded file string
        uploaded_file_url = fs.url(filename)
        # finds the person that defaultly upload the file. This is defaultly instantiated to the first user in the system
        username = request.user.username
        user = CustomUser.objects.get(username = username)
        # insertion is done here
        data = Data(name = name, path= uploaded_file_url, user = user)
        # data is save to database
        data.save()
        # create dataframe here 
        df = pd.read_csv('C:/Users/HP/projects/EmpAnalyst'+ urllib.parse.unquote(uploaded_file_url))
        # analyse the data here
        analyseData(df,ratio,data)
        return redirect('success',data.id)
    else:
        # form = DocumentForm()
        username = request.user.username
        return render(request, 'analyse.html',{'name':username, 'analyse':True})


      
  
