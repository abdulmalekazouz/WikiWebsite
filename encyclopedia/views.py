from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms
import re
import random

from . import util

class QueryForm(forms.Form):
    query = forms.CharField(
    label = "",
    widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

class TitleAreaNew(forms.Form):
    title = forms.CharField(
    label = "",
    widget=forms.TextInput(attrs={'placeholder': 'Title...'}))

class TextAreaNew(forms.Form):
    txt = forms.CharField(
    label = "",
    widget=forms.Textarea(attrs={'placeholder': 'Enter the Content (Markdown) ...'}))

class TitleAreaDisabled(forms.Form):
    title = forms.CharField(
    disabled = True,
    label = "",
    widget=forms.TextInput())



def index(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            queryString = str(query)

            y = '\A'+queryString
            matchentries = []

            for entry in util.list_entries():
                if(queryString == str(entry)):
                    return search(request,query)
                x = re.search(y,str(entry))
                if x:
                    matchentries.append((str(entry)))

            return render(request,"encyclopedia/pagesFound.html", {"entries":matchentries, "form":QueryForm()})

        else:
            return HttpResponse("Invalid entry, try again...")
    return render(request,"encyclopedia/index.html", {"entries": util.list_entries(), "form": QueryForm()})


def search(request, name):
    pageNotFound = False
    if (util.get_entry(name) == None):
        page = "<h1>Error, the page you are looking for could not be found...<h1>"
        pageNotFound = True
    else:
        page = Markdown().convert(util.get_entry(name))

    return render(request,"encyclopedia/searchPage.html", {"text": page, "form": QueryForm(), "entry":name, "notFound": pageNotFound})


def new(request):
    if request.method == "POST":
        titlearea = TitleAreaNew(request.POST)
        txtarea = TextAreaNew(request.POST)
        if titlearea.is_valid() and txtarea.is_valid():
            title = titlearea.cleaned_data["title"]
            txt = txtarea.cleaned_data["txt"]

            for entry in util.list_entries():
                if(title == str(entry)):
                    return render(request,"encyclopedia/pageAlreadyExists.html", {"form":QueryForm()})

            util.save_entry(title, txt)

        return search(request, str(title))

    return render(request,"encyclopedia/newPage.html", {"form": QueryForm(), "titlearea": TitleAreaNew(), "txtarea": TextAreaNew()})

def edit(request, entry):
    if request.method == "POST":
        txtarea = TextAreaNew(request.POST)
        if txtarea.is_valid():
            txt = txtarea.cleaned_data["txt"]
            util.save_entry(entry, txt)
            return search(request,entry)

        return search(request, str(title))
    return render(request,"encyclopedia/editPage.html", {"form": QueryForm(), "txtarea": TextAreaNew(initial={'txt': util.get_entry(entry)}), "titlearea": TitleAreaDisabled(initial={'title': entry}), "e":entry })


def rand(request):
    randnum = random.randrange(0,len((util.list_entries())))
    entrylist = util.list_entries()
    return search(request,entrylist[randnum])
