from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.safestring import mark_safe

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    markdown_entry = util.get_entry(title)
    entry = markdown2.markdown(markdown_entry)
    if not entry:
        return HttpResponseNotFound("<h1>Entry not found</h1>")
    return render(request, f"encyclopedia/entry.html",{
        "entry" : mark_safe(entry),
        "title" : title
    })
