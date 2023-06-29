from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import random
import markdown2
# import re

# Classes

class NewPage(forms.Form):
    title = forms.CharField(max_length=5)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))


# Functions

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    article = markdown2.markdown(util.get_entry(title))
    if not article:
        article = "The requested page was not found! Try another topic..."
    return render(request, "encyclopedia/entry.html", {
        "title"  : title,
        "article" : article
    })

def search(request):
    query = request.GET['q'].lower()
    listEntries = [entry.lower() for entry in util.list_entries()]
    if query in listEntries:
        return entry(request, query)
    else :
        entries = [entry for entry in listEntries if query in entry]

        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    
def createPage(request):
    pageTitle = "Create Page"
    if request.method == 'POST':
        # Set Variables
        listEntries = util.list_entries()
        title = request.POST['title']
        content = request.POST['content']
        data = {
            'title' : title,
            'content' : content
        }
        form = NewPage(initial=data)

        # Check if title is there
        if title in listEntries:
            message = 'Title is already existed.. Use another!'
            return render(request, "encyclopedia/createPage.html",{
                "form" : form,
                "message" : message,
                "pageTitle" : pageTitle,
                "viewName" : "newPage"
            })
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse('entry', args=[title]))
    
    return render(request, "encyclopedia/createPage.html",{
        "form" : NewPage(),
        "pageTitle" : pageTitle,
        "viewName" : "newPage"
    })

def editPage(request, title):
    pageTitle = "Edit Page"
    # GET request
    if request.method != 'POST' :
        article = util.get_entry(title)
        data = {
                'title' : title,
                'content' : article
            }
        form = NewPage(initial=data)
        return render(request, "encyclopedia/editPage.html",{
                    "form" : form,
                    'title' : title,
                    "pageTitle" : pageTitle,
                    "viewName" : "editPage"
                })
    else : 
        content = request.POST['content']
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse('entry', args=[title]))

def randomPage(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', args=[title]))

