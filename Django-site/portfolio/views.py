from django.shortcuts import render,  HttpResponse

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

