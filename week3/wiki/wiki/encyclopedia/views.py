from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_convert_html(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        content_html = markdowner.convert(content)
        return content_html

def entry(request, title):
    content_html = md_convert_html(title)
    md_content = util.get_entry(title)
    if content_html is not None:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content_html,
            "md_content": md_content
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "h1": "404",
            "h4": "Not Found",
            "messange": "The title was not found"
        })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        if title == "":
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        content_html = md_convert_html(title)
        md_content = util.get_entry(title)
        if content_html is not None:
            return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content_html,
            "md_content": md_content
        })
        else:
            list_entries = util.list_entries()
            list_substring = [entry for entry in list_entries if title in entry ]
            return render(request, "encyclopedia/search_result.html",{
                "entries": list_substring 
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create_new(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["new_content"]
        if title in util.list_entries():
            return render(request,"encyclopedia/error.html",{
            "h1": "ERROR",
            "h4": "",
            "messange": "The title of content already existed "
        })
        util.save_entry(title, content)

        content_html = md_convert_html(title)
        md_content = util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content_html,
            "md_content": md_content
        })
    return render(request, "encyclopedia/create_new.html")

def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })

def edit_result(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["edit_content"]
        util.save_entry(title, content)
        content_html = md_convert_html(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": content_html,
            "md_content":content
        })

def random_page(request):
    list_title = util.list_entries()
    random_title = random.choice(list_title)
    content_html = md_convert_html(random_title)
    md_content = util.get_entry(random_title)
    return render(request, "encyclopedia/entry.html",{
        "title": random_title,
        "content": content_html,
        "md_content": md_content
    })        

