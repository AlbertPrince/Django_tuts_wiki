from django import forms
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import util
import markdown2
import random

class Entry_Form(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    entry = forms.CharField(label="Your Entry", max_length=200)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    markdown_entry = util.get_entry(title)
    entry = markdown2.markdown(markdown_entry)
    if not markdown_entry:
        return render(request, "encyclopedia/error.html", {"message": "Entry not found"})
    return render(request, f"encyclopedia/entry.html",{
        "entry" : mark_safe(entry),
        "title" : title
    })
    
def random_entry(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect('entry', title=random_title)
    else:
        return redirect('index')
    
def create_entry(request):
    return render(request, "encyclopedia/create.html")

def edit_entry(request, title):
    pass
    
