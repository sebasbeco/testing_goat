from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List

# FIXME: remove hardcoded URLs

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todo_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': todo_list})


def new_list(request):
    todolist = List.objects.create()
    item = Item(text=request.POST['item_text'], list=todolist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        todolist.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{todolist.id}/')


def add_item(request, list_id):
    todo_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=todo_list)
    return redirect(f'/lists/{todo_list.id}/')