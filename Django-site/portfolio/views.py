from django.shortcuts import render,  HttpResponse
from .models import MyNotes

# Create your views here.
def index (req):

    params = {
                "page_title": "Python Portfolio Project",
                "tag": "welcome to my django project"
            }
    
    return render(req, "portfolio/index.html", params)



def about (req):

    params = {
                "page_title": "about me",
                "tag": "welcome, here is a little about me",
                "items": ["one", "two", "three"],

        }
    
    return render(req, "portfolio/about.html", params)

def docs (req):
    
    production_docs = MyNotes.objects.filter(draft=True)
    params = {
        "page_title": "My Notes",
        "tag": "Documentation and References",
        "notes": production_docs,
    }

    return render(req, "portfolio/docs.html", params)