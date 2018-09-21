import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path
import urllib

def naming_pn(i,date):
    date=str(date)
    name=str(i+1)+"."+date+".jpg"
    name=str(name)
    return name
def naming_vn(i,date):
    date=str(date)
    name=str(i+1)+".동영상"+date+".jpg"
    name=str(name)
    return name
def stacked_naming_pn(i,date):
    date=str(date)
    name=str(i)+"."+date+".jpg"
    name=str(name)
    return name
def stacked_naming_vn(i,date):
    date=str(date)
    name=str(i)+".동영상"+date+".jpg"
    name=str(name)
    return name

def get_url(vn,url):
    if vn==0:
        url=driver.find_element_by_class_name('eLAPa kPFhm').find_element_by_class_name('KL4Bh').get_attribute('src')
        return url
    else: None
def makedirname(dir,pagename):
    dirname="./"+pagename+"/"+date[0:7]
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def filenaming(pn,i,date):
    if pn==1:
        filename=naming_pn(i,date)
    else:
        None
    print(filename)
    return filename

def stackedfilenaming(pn,i,date):
    if pn ==1:
        filename=stacked_naming_pn(i,date)
    else:
        None
    print(filename)
    return(filename)

def download(vn,)
