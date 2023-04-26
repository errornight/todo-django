from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Task
from django.views.decorators.http import require_POST
from functools import wraps
from .forms import AddTaskForm, EditTaskForm

def cookie_check(view_func):
    # a decorator to check request cookie.
    # if there is user_id value, query and pass it to the function.
    # else generate an id, set it in clients search engin.
    def wrapper(request, *args, **kwargs):
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(public_id=user_id)
        else:
            user = User.objects.create()
            response = view_func(request, user, *args, **kwargs)
            response.set_cookie('user_id', user.public_id)
            return response

        return view_func(request, user, *args, **kwargs)

    return wrapper



@cookie_check
def home(request, user):
    # home page veiw!

    # query all tasks that are owned by the user and they are still in progress.
    tasks = Task.objects.filter(user=user, status= False).order_by('date_created')
    context = {'user': user, 'tasks': tasks}
    return render(request, 'main/home.html', context)


@cookie_check
def add_task(request, user):
   # add task view

   # check if the request method is POST, we create another task base on the request
   if request.method == 'POST':
       form = AddTaskForm(request.POST)
       if form.is_valid():
            form.save(user)
            return redirect('Home')
   else:
       form = AddTaskForm()
       
   context = {'user': user, 'form': form}
   return render(request, 'main/add-task.html', context)


@require_POST
@cookie_check
def remove_task(request, user, _id):
    # for deleting tasks, it gets task id and delete it.
    task = get_object_or_404(Task, user=user, id=_id)
    task.delete()
    return redirect('Home')


@cookie_check
def edit_task(request, user, _id):
   task = get_object_or_404(Task, user=user, id=_id, status=False)

   if request.method == 'POST':
       form = EditTaskForm(request.POST)
       if form.is_valid():
            form.save(task)
            return redirect('Home')
   else:
       form = EditTaskForm()
       
   context = {'task': task, 'form': form}
   return render(request, 'main/edit-task.html', context)


@cookie_check
@require_POST
def done_task(request, user, task_id):
    # change tasks status to DONE.

    task = get_object_or_404(Task, id=task_id, user=user)
    task.status = True
    task.save()

    # here we do not return any response, because we handle it with JS.

