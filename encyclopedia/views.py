from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown import markdown
import os, random

from . import util
from mdutils.mdutils import MdUtils
from mdutils import Html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, title):

    if request.method == 'POST':

        editted_content=request.POST.get('content')

        util.save_entry(title,editted_content)

        return HttpResponseRedirect(reverse("entry", args=(title,)))
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry_content": util.get_entry(title),
    })
    

def new(request):

    if request.method == 'POST':
        form=request.POST
        title=form.get('title')
        content=form.get('mkd_entry')
        entries = util.list_entries()

        for entry in entries:
            if title.lower() == entry.lower():
                return HttpResponse(f"This entry already exists!")

        f=open(f"entries/{title}.md", "w")
        f.write(f"#{title.capitalize()}\n\n\n")
        f.write(f"{content}")
        
        

        return HttpResponseRedirect(reverse("entry", args=(title,)))

    return render(request, "encyclopedia/new.html")
    

def entry(request, title):

    if util.get_entry(title) is None:

        return HttpResponse(f"No such entry found :(")
    else:
        
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_content": markdown(util.get_entry(title))
        })

def search(request):
    form=request.POST
    text=form.get('q')
    search_results=[]
    entries = util.list_entries()

    if not text is None:

        text=text.lower()

        for entry in entries:
            if text == entry.lower():
                title=entry
                return render(request, "encyclopedia/entry.html", {
                "title": title.capitalize(),
                "entry_content": markdown(util.get_entry(title))
                })

        for entry in entries:
           
            if text in entry.lower():
                search_results.append(entry)
                
        if not search_results:
            return render(request, "encyclopedia/search.html",{
                "text":f"No results for \"{text}\""
            })
        else:
            return render(request, "encyclopedia/search.html",{
                "text":f"Results for \"{text}\"",
                "search_results": search_results
            })
    
    return render(request, "encyclopedia/search.html",{
                "text":f"You must enter text to search!"
            })

def random_page(request):

    entries = util.list_entries()

    count= len(entries)

    title=entries[random.randint(0,count-1)]

    return HttpResponseRedirect(reverse("entry", args=(title,)))