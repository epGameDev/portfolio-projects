from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Note
import markdown

# Create your views here.
def index (req):

    params = {
        "page_title": "Python Portfolio Project",
        "tag": "welcome to my django project"
    }
    
    try:
        return render(req, "portfolio/index.html", params)
    except:
        raise Http404()


def about (req):

    params = {
        "page_title": "about me",
        "tag": "welcome, here is a little about me",
        "items": ["one", "two", "three"],
    }
    
    return render(req, "portfolio/about.html", params)


def contact (req):
    params = {
        "page_title": "about me",
        "tag": "shoot me a message anytime",
        "items": ["one", "two", "three"],
    }
    return render(req, "portfolio/contact.html", params)


def docs (req):
    
    production_docs = Note.objects.filter(draft=False)
    params = {
        "page_title": "My Notes",
        "tag": "Documentation and References",
        "notes": production_docs,
    }

    return render(req, "portfolio/docs.html", params)


def post (req, pk):
    md = markdown.Markdown(extensions=["fenced_code"])
    post = get_object_or_404(Note, id=pk, draft=False)
    post.content = md.convert(post.content)

    params = {
        "page_title": "Post",
        "tag": "My post",
        "post": post,
    }

    return render(req, "portfolio/post.html", params)