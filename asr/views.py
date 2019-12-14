# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
import time,random,urllib,codecs
import smtplib
from email.mime.text import MIMEText

import os.path
from os import path

from kws.views import Keyword
from django.conf import settings
from urllib.parse import unquote
# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'asr/index.html', context=None)



class RulesPageView(TemplateView):
    template_name = "asr/rules.html"

class RegisterPageView(TemplateView):
    template_name = "asr/register.html"

def registerUser(request):
    print('registerUser Request Received')
    if request.method == 'GET':
        user_database_folder ="asr/data/users"
        key_database_folder ="asr/data/keys"

        name = request.META['HTTP_NAME']
        age = request.META['HTTP_AGE']
        gender = request.META['HTTP_GENDER']
        mailid = request.META['HTTP_MAILID']

        if path.exists(user_database_folder+"/"+mailid+".txt"):
            return HttpResponse('User already exists')
        else:

            key = generateKey()
            new_user_file = open(user_database_folder+"/"+mailid+".txt","w+")
            new_user_file.write(name+"\n")
            new_user_file.write(age+"\n")
            new_user_file.write(gender+"\n")
            new_user_file.write(mailid+"\n")
            new_user_file.write(key+"\n")
            new_user_file.close()

            new_key_file = open(key_database_folder+"/"+key+".txt","w+")
            new_key_file.write(mailid)
            new_key_file.close()

            sendEmail(mailid,key)
            return HttpResponse('Registered successfully. Please check your mail for the key')
    else:
        print('Wrong Request Received')
        return HttpResponse('Faliure')

def sendEmail(mailid,key):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login("speech.data.gentool@gmail.com", "datagen4269")
    msg = MIMEText("Your Key: "+key)
    msg['From'] = 'speech.data.gentool@gmail.com'
    msg['To'] = mailid
    msg['Subject'] = 'Speech data generation key'
    s.sendmail("speech.data.gentool@gmail.com", mailid, msg.as_string())
    s.quit() 
    return 0

def generateKey():
    KEY_SIZE = 64
    key_database_folder ="../data/keys"
    key=""
    while True:
        key=""
        for i in range(0,KEY_SIZE):
            key = key + str('{:x}'.format(random.randrange(0,16,1)))
        if not path.exists(key_database_folder+"/"+key+".txt"):
            break
    return key


def checkKey(request):
    print('checkKey Request Received')
    if request.method == 'GET':
        key_database_folder ="asr/data/keys"
        key = request.META['HTTP_KEY']
        file_name = key_database_folder+"/"+key+".txt"
        if path.exists(file_name):
            id_file = open(file_name,"r")
            id = id_file.read()
            id_file.close()
            response = HttpResponse('Success')
            response['id'] = id
            return response
        else:
            return HttpResponse('Faliure')
    else:
        return HttpResponse('Faliure')

def uploadAudio(request):
    print('uploadAudio Request Received')
    if request.method == 'POST':
        user_database_folder ="asr/data/users"
        #text = urllib.unquote(request.META['HTTP_TEXT'])
        keywords = request.headers['text']
        #keywords = urllib.unquote(text).decode('utf-8')
        print(keywords)
        '''text = request.META['HTTP_TEXT']
        id = request.META['HTTP_ID']
        decoded_text = urllib.unquote(text).decode('utf-8')
        print(decoded_text)

        user_file_name = user_database_folder+"/"+id+".txt"

        user_file = open(user_file_name,"r")
        user_data = user_file.read().split('\n')
        user_file.close()
        
        #saving the file
        '''
        
        
        keyword = Keyword()
        keyword.make_raw_list(keywords.split(','))

        file_name= "recorded-" + str(time.time())+".wav"
        file_16_path = settings.USER['kaldi']['kws_upload']+'/'+file_name
        file_41_path = 'asr/data/voice_samples/' + file_name
        
        uploadedFile = open(file_41_path, "wb")
        uploadedFile.write(request.body)
        uploadedFile.close()
        print('wav file saved')
        
        sox_change_to_16k(file_41_path, file_16_path)
        
        asr_script(file_16_path)

        with open('result_asr') as f:
            result_asr = f.readline()

       
        print(result_asr+'\n')

        file_list = [file_16_path]
        keyword.make_spk_utt(settings.USER['kaldi']['kws_upload'], file_list)
        keyword.run_kaldi_script()
        #record_file = codecs.open("asr/data/record.txt","a+",'utf-8')
        #record_file.write(file_name+" "+decoded_text)
        #record_file.close()
        print('record file updated')
        return HttpResponse('Success')
    
    else:
        print('Wrong Request Received')
        return HttpResponse('Faliure')


def asr_script(wav_file_path):
    print("bash asr/asr.sh "+os.path.abspath(wav_file_path)+" > result_asr")
    os.system("bash asr/asr.sh "+os.path.abspath(wav_file_path)+" > result_asr")

def sox_change_to_16k(old_path, new_path):
    os.system('sox '+old_path+' -r 16000 -c 1 -b 16 '+new_path)


def getText(request):
    print('getText Request Received')
    text =""
    if request.method == 'GET':
        num_text = 100

        last_text_num = int(request.META['HTTP_NUM'])

        while True:
            random_number = random.randint(0,num_text-1)
            if random_number == last_text_num:
                print('Collison Occured')
            else:
                break
        
        file_name = "asr/data/text_samples/"+str(random_number)+".txt"
        text_file = open(file_name,"r")
        text = text_file.read()
        text_file.close()
        
        response = HttpResponse(text)
        response['num'] = random_number
        return response
    else:
        print('Wrong Request Received')
        return HttpResponse('Faliure')
    
