from django import forms
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages

from . import util
import markdown2
import random

class Entry_Form(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    entry = forms.CharField(widget=forms.Textarea, label="Markdown Content", max_length=200)
    
class Edit_Form(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Markdown Content", max_length=200)


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
    if request.method == "POST":
        form = Entry_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            
            if util.get_entry(title):
                messages.error(request, f"An entry with the title '{title}' already exists.")
                return render(request, 'encyclopedia/create.html', {'form': form})
            util.save_entry(title, content)
            return redirect('entry', title=title)
        else:
            return render(request, "encyclopedia/create.html", {
                "form" : form
            })
    return render(request, "encyclopedia/create.html", {
        "form" : Entry_Form()
    })

def edit_entry(request, title):
    if request.method == "POST":
        form = Edit_Form(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(entry, title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
        "form" : form
    }) 
    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "form" : Edit_Form()
    })
  
    # existing_content = util.get_entry(title)
    # if existing_content is None:
    #     return render(request, 'encyclopedia/error.html')

    # if request.method == 'POST':
    #     form = Edit_Form(request.POST)
    #     if form.is_valid():
    #         new_content = form.cleaned_data['content']
    #         util.save_entry(title, new_content)
    #         return redirect('entry', title=title)
    # else:
    #     form = Edit_Form(initial={'content': existing_content})
    
    # return render(request, 'encyclopedia/edit.html', {'form': form, 'title': title})


def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if util.get_entry(query):
            return redirect('entry', title=query)
        else:
            matched_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            return render(request, 'encyclopedia/search.html', {
                "matched_entries": matched_entries,
                "query": query
            })
    return render(request, 'encyclopedia/search.html')
            
