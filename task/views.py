from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,CustomerForm,TaskForm,NoteForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
# Create your views here.

# @login_required(login_url='login')
def editText(request):
	output = {}
	if request.method == "GET" and request.is_ajax():
		Type = request.GET['type']
		Id = request.GET['id']
		New_text = request.GET['new_text']

		try:
			Id = int(Id)
		except:
			output['status'] = False
			return JsonResponse(output)

		if Type in ['task', 'note']:
			output['new_text'] = New_text
			if Type == 'task':
				focused_task = myTask.objects.filter(id = Id)
				if focused_task.exists():
					focused_task = focused_task[0]
					focused_task.task_text = New_text
					focused_task.save()
					output['status'] = True
			else:
				focused_note = myNote.objects.filter(id = Id)
				if focused_note.exists():
					focused_note = focused_note[0]
					focused_note.note_text = New_text
					focused_note.save()
					output['status'] = True
		else:
			output['status'] = False

		print(Type, Id, New_text)
		output['type'] = Type
		output['id'] = Id

	return JsonResponse(output)


@login_required(login_url='login')
def operation(request):
	output = {}
	if request.method == "GET" and request.is_ajax():
		sign = request.GET['sign']
		task_id = int(request.GET['id'])

		myQuery = myTask.objects.filter(id = task_id)
		if myQuery.exists():
			focused_task = myQuery[0]
			if focused_task.added_by == request.user:
				if sign == "delete":
					focused_task.delete()
					output['status'] = True
					output['message'] = "Task is being deleted..."
				elif sign == "complete":
					focused_task.complete_now()
					output['status'] = True
					output['message'] = "Task is being marked as completed..."
			else:
				output['status'] = False
				output['message'] = "This task doesn't belong to you"
		else:
			output['status'] = False
			output['message'] = "Something went wrong"

	return JsonResponse(output)


@login_required(login_url='login')
def operation_note(request):
	output = {}
	if request.method == "GET" and request.is_ajax():
		sign = request.GET['sign']
		note_id = int(request.GET['id'])

		myQuery = myNote.objects.filter(id = note_id)
		if myQuery.exists():
			focused_note = myQuery[0]
			if focused_note.added_by == request.user:
				if sign == "delete":
					focused_note.delete()
					output['status'] = True
					output['message'] = "Note is being deleted..."
			else:
				output['status'] = False
				output['message'] = "This note doesn't belong to you"
		else:
			output['status'] = False
			output['message'] = "Something went wrong"

	return JsonResponse(output)



@login_required(login_url='login')
def customer_view(request, customer_id):
	try:
		context = {
			'today': datetime.now().date()
		}
		ID = int(customer_id)
		if Customer.objects.filter(id = ID, added_by = request.user).exists() or ID == 0:
			if ID == 0:
				context['my_customer'] = None
			else:
				context["my_customer"] = Customer.objects.get(id = ID)
				
			if request.method == "POST":
				if 'newTask' in request.POST:
					newTask = request.POST['newTask']
					dueOn = request.POST['dueOn']

					if request.POST['dueOn'] != "":
						due_date_entered = dueOn
					else:
						due_date_entered = datetime.now().date()
					# print('dueOn' in request.POST and request.POST['dueOn'])
					
					new_task = myTask(
						task_text = newTask,
						due_date = due_date_entered,
						added_by = request.user,
						added_for = context['my_customer']
					)
					new_task.save()
					messages.info(request, "New task has been added successfully!")

				if 'newNote' in request.POST and request.POST['newNote'] != "":
					newNote = request.POST['newNote']
					new_note = myNote(
						note_text = newNote,
						added_by = request.user,
						added_for = context['my_customer']
					)
					new_note.save()
					messages.error(request, "New note has been added successfully!")

					# return redirect("customer/"+str(context['my_customer'].id))
			all_tasks = myTask.objects.filter(added_by = request.user, added_for = context['my_customer']).order_by('-id')
			all_notes = myNote.objects.filter(added_by = request.user, added_for = context['my_customer']).order_by('-id')
			
			for task in all_tasks:
				if task.due_date < datetime.now().date():
					task.late_now()
			
			context['all_tasks'] = all_tasks
			context['all_notes'] = all_notes
			context['customers'] = Customer.objects.filter(added_by = request.user).order_by('first_name')
			context['temp'] = True
			return render(request, "task/customer.html", context)
		else:
			return redirect("home page")
	except:
		return redirect("home page")



@login_required(login_url='login')
def search(request):
	# try:
		if request.method == "GET" and request.GET['query'] != "":
			context = {
				'today': datetime.now().date()
			}
			query = request.GET['query']

			if len(query) > 30:
				query_to_show = query[0: 30]+"..."
			else:
				query_to_show = query
				
			all_tasks = myTask.objects.filter(added_by = request.user, task_text__contains=query).order_by('-id')
			all_notes = myNote.objects.filter(added_by = request.user, note_text__contains=query).order_by('-id')
			
			for task in all_tasks:
				if task.due_date < datetime.now().date():
					task.late_now()
			
			context['query_to_show'] = query_to_show
			context['query'] = request.GET['query']
			context['all_tasks'] = all_tasks
			context['all_notes'] = all_notes
			context['customers'] = Customer.objects.filter(added_by = request.user).order_by('first_name')
			context['customer_section'] = True
			context['temp'] = True
			return render(request, "task/customer.html", context)
		else:
			return redirect("home page")
	# except:
	# 	return redirect("home page")





@login_required(login_url='login')
def index(request):
	# form=CustomerForm()
	customers=Customer.objects.filter(added_by = request.user).order_by('first_name')
	
	if request.method=='POST':
		new_customer = Customer(
			account_name = request.POST['account_name'], 
			renewal_date = request.POST['renewal_date'],
			revenue = request.POST['revenue'],
			added_by = request.user
		)
		new_customer.save()
		return redirect('home page')
	
	all_tasks = myTask.objects.filter(added_by = request.user).order_by('-id')
	
	for task in all_tasks:
		if task.due_date < datetime.now().date():
			task.late_now()
	
	context = {'customers':customers}
	context['all_tasks'] = all_tasks
	context['customer_section'] = True
	context['today'] = datetime.now().date()
	return render(request,'task/index.html', context)


def delete_items(request, pk):
	data = Customer.objects.get(id=pk)
	if request.method == 'POST':
		data.delete()
		# messages.success(request,'successfully deleted')
		return redirect('home page')
	return render(request, 'task/task_confirm_delete.html')





def register(request):


	form=UserRegistrationForm()

	if request.method=='POST':

		form=UserRegistrationForm(request.POST)

		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,f'Your account has been created, Login now')

			return redirect('login')
		
			
	return render(request,'task/register.html',{'form':form})   



def task(request):
	tasks=Task.objects.all()
	form=TaskForm()
	if request.method=='POST':
		form=TaskForm(request.POST)
		if form.is_valid():
			form.save()

			return redirect('task')

	return render(request,'task/task.html',{'form':form,'tasks':tasks})





def update(request,id):
    
    if request.method=='POST':
        data=Task.objects.get(pk=id)
        fm=TaskForm(request.POST,instance=data)
        if fm.is_valid():
            fm.save()
            return redirect('task')
    else:
        data=Task.objects.get(pk=id)
        fm=TaskForm(instance=data)   
      
    return render(request,'task/edit.html',{"form":fm})



def delete(request, pk):
	data = Task.objects.get(id=pk)
	if request.method == 'POST':
		data.delete()
		# messages.success(request,'successfully deleted')
		return redirect('task')
	return render(request, 'task/delete.html')




def note(request):
	notes=Note.objects.all()
	form=NoteForm()
	if request.method=='POST':

		form=NoteForm(request.POST)

		if form.is_valid():
			form.save()

			return redirect('note')

	return render(request,'task/note.html',{'form':form,'notes':notes})



def update_note(request,id):
    
    if request.method=='POST':
        data=Note.objects.get(id=id)
        fm=NoteForm(request.POST,instance=data)
        if fm.is_valid():
            fm.save()
            return redirect('note')
    else:
        data=Note.objects.get(id=id)
        fm=NoteForm(instance=data)   
      
    return render(request,'task/note_edit.html',{"form":fm})



def delete_note(request, id):
	data = Note.objects.get(id=id)
	if request.method == 'POST':
		data.delete()
		# messages.success(request,'successfully deleted')
		return redirect('note')
	return render(request, 'task/note_delete.html')


def logout(request):
    auth.logout(request)
    return redirect("home page")