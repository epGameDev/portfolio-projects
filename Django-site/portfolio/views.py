from django.shortcuts import render,  HttpResponse

# Create your views here.
def index (req):

    params = {
                "page_title": "Python Portfolio Project",
                "code": "python"
            }
    
    return render(req, "portfolio/index.html", params)



def about (req):

    params = {
                "page_title": "about me",
                "title": "welcome, here is a little about me",
                "items": ["one", "two", "three"],

        }
    
    return render(req, "portfolio/about.html", params)



def projects (req, project_name):
    return HttpResponse(f"Welcome to my {project_name} project!")

def add (req, num1, num2):
    total = num1 + num2
    return HttpResponse(f"Your total is: {total}")