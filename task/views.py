from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,CustomerForm,TaskForm,NoteForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
import json
import csv


@login_required(login_url='login')
def reset_password(request):
	if request.method == "POST":
		current_password = request.POST['current']
		new_password = request.POST['new']
		confirm_new_password = request.POST['confirm']

		if check_password(current_password, request.user.password):
			if new_password == confirm_new_password:
				request.user.set_password(new_password)
				request.user.save()
				messages.error(request, "Your password has been changed successfully!")
				
			else:
				messages.error(request, "New password and confirm password fields doesn't match!")
		else:
			messages.error(request, "Current password is not correct!")
		return redirect("home page")
	else:
		return redirect("home page")




# Create your views here.
@login_required(login_url='login')
def addFields(request):
	output = {}
	if request.method == "GET" and request.is_ajax():
		try:
			my_fields = request.GET['myFields']
			myFieldDict = json.loads(my_fields)

			for field in myFieldDict:
				if field:
					new_field = myField(
						user = request.user,
						field_name = field['field_name'],
						field_type = field['type'],
						is_requied = (field['required'] == 'yes')
					)

					new_field.save()

			new_status = dynamicFieldStatus(user = request.user)
			new_status.save()
			output['status'] = True
		except:
			output['status'] = False

	return JsonResponse(output)


@login_required(login_url='login')
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
			if Type == 'task':
				focused_task = myTask.objects.filter(id = Id)
				if focused_task.exists():
					focused_task = focused_task[0]
					focused_task.task_text = New_text
					focused_task.save()
					output['status'] = True
					output['new_text'] = New_text
			else:
				focused_note = myNote.objects.filter(id = Id)
				if focused_note.exists():
					focused_note = focused_note[0]
					focused_note.note_text = New_text
					focused_note.save()
					output['status'] = True
					output['new_text'] = focused_note.text_with_line()
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
					output['message'] = "Task is being marked as complete..."
				elif sign == "incomplete":
					focused_task.incomplete_now()
					output['status'] = True
					output['message'] = "Task is being marked as incomplete..."
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

			late_tasks = list(myTask.objects.filter(added_by = request.user, added_for = context['my_customer'], status = -1))
			bubbleSort(late_tasks)
			open_tasks = list(myTask.objects.filter(added_by = request.user, added_for = context['my_customer'], status = 0))
			bubbleSort(open_tasks)
			completed_tasks = list(myTask.objects.filter(added_by = request.user, added_for = context['my_customer'], status = 1))
			bubbleSort(completed_tasks)

			all_tasks = late_tasks + open_tasks + completed_tasks

			all_notes = myNote.objects.filter(added_by = request.user, added_for = context['my_customer']).order_by('-id')
			
			
			for i in all_notes:
				print(i.text_with_line())

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


def bubbleSort(arr):
    n = len(arr)
  
    # Traverse through all array elements
    for i in range(n-1):
    # range(n) also work but outer loop will repeat one time more than needed.
  
        # Last i elements are already in place
        for j in range(0, n-i-1):
  
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j].due_date > arr[j+1].due_date :
                arr[j], arr[j+1] = arr[j+1], arr[j]


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
				
			late_tasks = list(myTask.objects.filter(added_by = request.user, task_text__contains=query, status = -1))
			bubbleSort(late_tasks)
			open_tasks = list(myTask.objects.filter(added_by = request.user, task_text__contains=query, status = 0))
			bubbleSort(open_tasks)
			completed_tasks = list(myTask.objects.filter(added_by = request.user, task_text__contains=query))
			bubbleSort(completed_tasks)

			all_tasks = late_tasks + open_tasks + completed_tasks
			
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

def find_index(user_field, given_headers):
	given_headers = list(map(lambda x: x.lower(), given_headers))
	searched_index = None
	for i in range(len(given_headers)):
		if user_field.lower() in given_headers[i]:
			searched_index = i
			break
	return searched_index

def is_allow(all_fields_of_user, given_headers):
	searched_index = None
	name_related_field = None
	status = True
	replica = list(map(lambda x: x.lower(), given_headers))
	print(given_headers)

	condition1 = ("account" in replica)
	condition2 = ("account name" in replica)
	condition3 = ("account_name" in replica)

	if condition1 or condition2 or condition3:
		for i in range(len(replica)):
			if "account" in replica[i]:
				searched_index = i
				break
		
		status = True
			
		for single_field in all_fields_of_user:
			if single_field.field_name.lower() not in replica:
				status = False
				break
	else:
		status = False

	return {
		"status": status,
		"name_field_index": searched_index
	}


@login_required(login_url='login')
def index(request):
	# form=CustomerForm()
	context = {}
	customers=Customer.objects.filter(added_by = request.user).order_by('first_name')
	context['all_fields'] = myField.objects.filter(user = request.user)

	if request.method=='POST':
		if 'account_name_special' in request.POST:
			new_customer = Customer(
				account_name = request.POST['account_name_special'], 
				added_by = request.user
			)
			new_customer.save()

			for single_field in context['all_fields']:
				enterd_value = request.POST[single_field.field_name]
				print(enterd_value)
				new_sing_field_value = myFieldValue(
					field = single_field,
					value = enterd_value,
					customer = new_customer
				)

				new_sing_field_value.save()

			messages.info(request, "Account has been created successfully!")
			return redirect('home page')

		if 'editingFields' in request.POST:
			for i, j in request.POST.items():
				if "_" in i:
					field_id = int(i.split("_")[1])
					focused_field = myField.objects.filter(id = field_id)
					if focused_field.exists():
						focused_field = focused_field[0]
						focused_field.field_name = j
						focused_field.save()
						# print(field_id, "=>", j)

			messages.error(request, "Account field names has been updated!")
		else:
			myAccountFile = request.FILES['myaccountfile']
			file_data = myAccountFile.read().decode("utf-8")	
			my_whole_data = []
			lines = file_data.split("\r\n")
			headers = lines[0].split(",")

			for index in range(1,len(lines)):
				line = lines[index]	
				if len(line) > 3:
					single_zip = zip(headers, line.split(","))
					my_whole_data.append(
						dict(single_zip)
					)


			print(my_whole_data)
			conditioning = is_allow(context['all_fields'], headers) 
			if conditioning['status']:
				for single_account in my_whole_data:

					new_customer = Customer(
						account_name = single_account[headers[conditioning['name_field_index']]], 
						added_by = request.user
					)
					new_customer.save()

					for single_field in context['all_fields']:
						enterd_value = single_account[headers[find_index(single_field.field_name, headers)]]
						new_sing_field_value = myFieldValue(
							field = single_field,
							value = enterd_value,
							customer = new_customer
						)

						new_sing_field_value.save()

				messages.info(request, "All accounts have been created successfully!")
			else:
				messages.info(request, "CSV file doesn't contain required parameters!")
			
			return redirect('home page')

	
	late_tasks = list(myTask.objects.filter(added_by = request.user, status = -1))
	bubbleSort(late_tasks)
	open_tasks = list(myTask.objects.filter(added_by = request.user, status = 0))
	bubbleSort(open_tasks)
	completed_tasks = list(myTask.objects.filter(added_by = request.user, status = 1))
	bubbleSort(completed_tasks)

	all_tasks = late_tasks + open_tasks + completed_tasks
	
	for task in all_tasks:
		if task.due_date < datetime.now().date():
			task.late_now()
	
	context['customers'] = customers
	context['all_tasks'] = all_tasks
	context['customer_section'] = True
	context['today'] = datetime.now().date()
	context['is_dynamic_field_added'] = dynamicFieldStatus.objects.filter(user = request.user).exists()
	context['my_all_fields'] = myField.objects.filter(user = request.user)
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