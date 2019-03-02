from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List

# FIXME:
#  remove duplicate validation logic

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    todolist = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=todolist)
            item.full_clean()
            item.save()
            return redirect(todolist)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': todolist, 'error': error})


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
    return redirect(todolist)