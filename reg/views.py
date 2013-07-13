from reg.forms import loginForm,studentRegistrationForm , clientRegistrationForm
from django.contrib.auth.models import Group
from testa import settings
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django import forms
from reg.models import userInfo
import string,random
from quiz.forms import quizForm 
from users.models import client,student
from django.core.mail import send_mail

def index(request):
	form = loginForm
	return render_to_response('index.html', {'loginform':form} , context_instance=RequestContext(request))
	
	
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def checklogin(request):
	form = loginForm(request.POST)	
	if form.is_valid():
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
	else:
		return HttpResponse('Form has errors')
	if user is not None:
		if user.is_active:
			login(request, user)
			if user.groups.filter(name='Client').exists():
				request.session['group'] = 'client'
				return HttpResponseRedirect('/client-dashboard/')
			else:
				request.session['group'] = 'student'
				return HttpResponseRedirect('/student-dashboard/')
		else:
			message = 'Your account is not yet activated'
			return render_to_response('index.html', {'loginform':form,'message':message} , context_instance=RequestContext(request))	
	else:
		message = 'Bad Username/Password'
		return render_to_response('index.html', {'loginform':form,'message':message} , context_instance=RequestContext(request))
	
	
def student_reg(request):
	if request.method == 'POST':
		form = studentRegistrationForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			year = form.cleaned_data['year']
			department = form.cleaned_data['department']
			college = form.cleaned_data['college']
			phone = form.cleaned_data['phone']
			full_name = first_name + ' ' + last_name
			if User.objects.filter(username=username).count()>0:
				loginform = loginForm
				form = studentRegistrationForm
				errors = 'Username already exists'
				return render_to_response('student-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))
			if User.objects.filter(email=email).count()>0:
				loginform = loginForm
				form = studentRegistrationForm
				errors = 'Email already exists'
				return render_to_response('student-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))			
			u = User.objects.create_user(username, email, password)
			u.is_active = False 
			u.groups.add(Group.objects.get(name = 'Student'))
			u.save()
			a_string = ''.join(random.choice(string.lowercase + string.digits)for x in range(30))
			user_info = userInfo(user = u,activation_string = a_string, name = full_name)
			user_info.save()
		#	mail_subject = 'Activate your account'
		#	mail_message = """Thank you for registering. You can activate your account by following the link.
		#						""" 
		#	mail_message+= """testapp.ungineering.com/activate/""" + user_info.activation_string 
		#	mail_from = 'noreply@testapp.com'
		#	mail_to = 'svksaha91@gmail.com'
		#	send_mail(mail_subject, mail_message,mail_from, [mail_to], fail_silently=False)
			s = student(userinfo = user_info,year=year,department=department,college=college,phone = phone)
			 
			s.save()
		else:
			errors = form.errors
			loginform = loginForm
			form = studentRegistrationForm
			return render_to_response('student-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))
						
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		
		loginform = loginForm
		form = studentRegistrationForm
		return render_to_response('student-registration.html', {'loginform':loginform,'form':form} , context_instance=RequestContext(request))
		
		
def client_reg(request):
	if request.method == 'POST':
		form = clientRegistrationForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			details = form.cleaned_data['details']
			full_name = first_name + ' ' + last_name
			if User.objects.filter(username=username).count()>0:
				errors = 'Username already exists'
				loginform = loginForm
				form = clientRegistrationForm
				return render_to_response('student-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))
			if User.objects.filter(email=email).count()>0:
				loginform = loginForm
				form = clientRegistrationForm				
				errors = 'Email already exists'
				return render_to_response('student-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))
			u = User.objects.create_user(username, email, password)
			u.is_active = False 
			u.groups.add(Group.objects.get(name = 'Client'))
			u.save()
			a_string = ''.join(random.choice(string.lowercase + string.digits)for x in range(30))
			user_info = userInfo(user = u,activation_string = a_string, name = full_name)
			user_info.save()
		#	mail_subject = 'Activate your account'
		#	mail_message = """Thank you for registering. You can activate your account by following the link.
		#						""" 
		#	mail_message+= """testapp.ungineering.com/activate/""" + user_info.activation_string 
		#	mail_from = 'noreply@testapp.com'
		#	mail_to = 'svksaha91@gmail.com'
		#	send_mail(mail_subject, mail_message,mail_from, [mail_to], fail_silently=False)
			c = client(userinfo = user_info,details=details) 
			c.save()	
		else:
			errors = form.errors
			loginform = loginForm
			form = clientRegistrationForm
			return render_to_response('client-registration.html', {'loginform':loginform,'form':form,'errors':errors} , context_instance=RequestContext(request))	
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		loginform = loginForm
		form = clientRegistrationForm
		return render_to_response('client-registration.html', {'loginform':loginform,'form':form} , context_instance=RequestContext(request))	

def activate_user(request,a_string):
	form = loginForm
	user = userInfo.objects.get(activation_string = a_string)
	user.user.is_active= True
	user.user.save()
	message = 'Account activated. Please login'
	return render_to_response('index.html', {'loginform':form,'message':message} , context_instance=RequestContext(request))
	
	
def change_password(request):
	if request.user.is_authenticated():
		if request.user.groups.filter(name = 'Client').exists():
			return render_to_response('client-change-password.html',context_instance=RequestContext(request))
		elif request.user.groups.filter(name = 'Student').exists():
			return render_to_response('student-change-password.html',context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def change_password_handler(request):
	if request.method == 'POST':
		if request.user.groups.filter(name = 'Client').exists():
			check = authenticate(username = request.user.username,password = request.POST['old_password'])
			if check is not None:
				user = request.user
				user.set_password(request.POST['new_password'])
				user.save()
				return render_to_response('client-change-password.html',{'message':'Password Changed'},context_instance=RequestContext(request))
			else:
				return render_to_response('client-change-password.html',{'message':'Wrong Password'},context_instance=RequestContext(request))
		elif request.user.groups.filter(name = 'Student').exists():
			check = authenticate(username = request.user.username,password = request.POST['old_password'])
			if check is not None:
				user = request.user
				user.set_password(request.POST['new_password'])
				user.save()
				return render_to_response('student-change-password.html',{'message':'Password Changed'},context_instance=RequestContext(request))
			else:
				return render_to_response('student-change-password.html',{'message':'Wrong Password'},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

def forgot_password(request):
	return render_to_response('forgot_password.html',context_instance=RequestContext(request))
			
def forgot_password_email(request):
	email = request.POST['email']
	user = userInfo.objects.get(user = User.objects.get(email=email))
	fp_string = ''.join(random.choice(string.lowercase + string.digits)for x in range(30))
	user.forgot_password_string = fp_string
	user.save()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	
def forgot_password_handler(request,fp_string):
	user = userInfo.objects.get(forgot_password_string=fp_string)
	request.session['fp_user'] = user.user
	return render_to_response('new_password.html',context_instance=RequestContext(request))
	
def new_password(request):
	password = request.POST['password']
	user = request.session['fp_user']
	user.password = password
	user.save()
	return HttpResponse('Password Changed')
		


