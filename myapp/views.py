from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt 


def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    errors = User.objects.regValidator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hash.decode())
        request.session['user_id'] = user.id
        return redirect("/dashboard")
 
def login(request):
    result = User.objects.loginValidator(request.POST)
    print(result)

    if result[0]:
        for key, value in result[0].items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        request.session["user_id"] = result[1].id
        return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")
    
def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['user_id'])
        all_lists = wishList.objects.all()
        lists_liked = user.liked.all()

        context = {
            "user": user, 
            "all_lists": all_lists,
            "lists_liked": lists_liked,
            "other_lists": all_lists.difference(lists_liked)
        }
        return render(request, "dashboard.html", context)

def add(request):
    return render(request, "add.html")

#def newList(request):
    #return render(request, "newList.html")

def create(request):
    user = User.objects.get(id=request.session['user_id'])
    errors = wishList.objects.wishlistValidator(request.POST)
    print(errors)

    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/add")
    else:
        lists = wishList.objects.create(item_product = request.POST['item_product'], added_by_id = request.session['user_id'])
        user.liked.add(lists)

        return redirect(f"/viewList/{lists.id}")
        
def viewList(request, lists_id):
    lists = wishList.objects.get(id=lists_id)
    all_users = lists.liked_by.all()
    
    context = {
        "lists": lists,
        "all_users": all_users.exclude(id=lists.added_by_id)
    }
    return render(request, "viewList.html", context)

def likeList(request, lists_id):
    lists = wishList.objects.get(id = lists_id)
    user = User.objects.get(id = request.session["user_id"])
    user.liked.add(lists)
    return redirect("/dashboard")

def removeList(request, lists_id):
    lists = wishList.objects.get(id = lists_id)
    user = User.objects.get(id = request.session["user_id"])
    user.liked.remove(lists)
    return redirect("/dashboard")

def delete(request, lists_id):
    lists_to_delete = wishList.objects.get(id=lists_id)	
    lists_to_delete.delete()
    return redirect("/dashboard")