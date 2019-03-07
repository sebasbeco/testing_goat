from django.shortcuts import render, redirect

from lists.forms import ItemForm
from lists.models import List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    todolist = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=todolist)
            return redirect(todolist)
    return render(request, 'list.html', {'list': todolist, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        todolist = List.objects.create()
        form.save(for_list=todolist)
        return redirect(todolist)
    else:
        return render(request, 'home.html', {'form': form})