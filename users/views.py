from reg.forms import loginForm,studentRegistrationForm , clientRegistrationForm
from django.contrib.auth.models import Group
from testa import settings
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django import forms
from reg.models import userInfo
import string,random
from quiz.forms import quizForm 
from users.models import client,student
from quiz.models import quiz,StudentTest,StudentTestQA,testQuestion
import datetime
from django.utils import timezone,simplejson
from math import ceil
from django.db.models import Q




def open_tests(request):
	now = timezone.now()
	tests = quiz.objects.filter(end_time__gte = now.strftime('%Y-%m-%d %X'),type='1')
	testlist = []
	
	for t in tests:
		details = {}
		details['id']=t.id
		details['client'] = t.client.userinfo.name
		details['title'] = t.title
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		details['test_key'] = t.key
		if StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz = t,score__isnull = False).count()>0:
			continue
 		testlist.append(details)		
	return testlist
#	except:
	#	return HttpResponse('no tests')
	
def closed_tests(request):
	now = timezone.now()
	tests = quiz.objects.filter(end_time__gte = now.strftime('%Y-%m-%d %X'),type='2')
	testlist = []
	for t in tests:
			
		details = {}
		details['id']=t.id
		details['client'] = t.client.userinfo.name
		details['title'] = t.title
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		details['test_id'] = t.id
		details['test_key'] = t.key
#		x = simplejson.loads(t.applicationJSON)		
#		details['no_q']= x['0']
#		del x['0']
#		details['apply_questions'] = x
		#applied is wrong
		if StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz = t,approved=True).count()>0:
			continue
		if StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz = t,score__isnull = False).count()>0:
			continue
 		testlist.append(details)		
	return testlist
	
def applied_tests(request):
	now = timezone.now()
	tests = quiz.objects.filter(end_time__gte = now.strftime('%Y-%m-%d %X'),type='2')
	testList = []
	for t in tests:
		stlist = StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz = t,apply_datetime__isnull = False,test_datetime__isnull = True,approved = False)
		if stlist.count() == 1:
			st = stlist[0]
			details = {}
			details['test_id'] = st.quiz.id
			details['client'] = st.quiz.client.userinfo.name
			details['title'] = st.quiz.title
			details['end_date'] = st.quiz.end_time
			details['duration'] = st.quiz.duration
			details['length'] = st.quiz.number_of_questions
			testList.append(details)
		else:
			continue
	return testList

def ongoing_tests(request):
	testList = []
	stlist = StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),taken = False)
	for st in stlist:
		details = {}
		details['test_id'] = st.quiz.id
		details['test_key'] = st.quiz.key
		details['client'] = st.quiz.client.userinfo.name
		details['title'] = st.quiz.title
		testList.append(details)
	return testList

def taken_tests(request):
	stlist =	StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),test_datetime__isnull = False).exclude(score='')
	testList = []
	for st in stlist:
		details = {}
		details['test_id'] = st.quiz.id
		details['client'] = st.quiz.client.userinfo.name
		details['title'] = st.quiz.title
		details['datetime'] = st.test_datetime
		details['score'] = st.score
		testList.append(details)
	return testList

def client_tests(request):
	tests = quiz.objects.filter(client = client.objects.get(userinfo = userInfo.objects.get(user = request.user)))
	testlist = []
	
	for t in tests:
		details = {}
		details['title'] = t.title
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		details['test_link'] = t.key
		stests= StudentTest.objects.filter(quiz = t)
		studentList = []
		for st in stests:
			 student_details = {}
			 student_details['name'] = st.student.userinfo.name
			 if st.apply_datetime == None:
			 	student_details['type'] = 'taken'
			 else:
			 	student_details['type'] = 'applied'
			 student_details['result1'] = st.score
			 student_details['finish_time'] = st.finsih_datetime
			 studentList.append(student_details)
		details['students'] = studentList
 		testlist.append(details)		
	return testlist


def test_applications(request):
	tests = quiz.objects.filter(client = client.objects.get(userinfo = userInfo.objects.get(user = request.user)))
	st_list = []	
	for t in tests:
		try:
			st = StudentTest.objects.get(quiz = t)
		except:
			continue
		if st.apply_datetime != None:
			st_list.append(st)
	
	applicationList = []
	for a in st_list:
		if a.approved == True:
			continue
	 	details = {}
	 	details['st_id']= a.id
		details['student_name'] = a.student.userinfo.name
		details['test_name'] = a.quiz.title
		details['apply_datetime'] = a.apply_datetime
		applicationList.append(details)		
		
	return applicationList

def approve_test(request):
	if request.user.groups.filter(name = 'Client').exists():
		ids = request.POST['approve'].split(',')
		for i in ids:
			st = StudentTest.objects.get(pk = int(i))
			if st.quiz.client.userinfo.user == request.user:
				st.approved = True
				st.save()
				return HttpResponse('Approved')
			else:
				return HttpResponse('You have a major bug in code')
	else:
		return HttpReponse('You are not a Client')
		
def test_analysis(request,test_id):
	stlist =	StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),test_datetime__isnull = False).exclude(score='')
	takenList = []
	for st in stlist:
		details = {}
		details['test_id'] = st.quiz.id
		details['client'] = st.quiz.client.userinfo.name
		details['title'] = st.quiz.title
		details['datetime'] = st.test_datetime
		details['score'] = st.score
		takenList.append(details)
	
	students = StudentTest.objects.filter(quiz_id = test_id,taken = True)
	st = StudentTest.objects.get(student=student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz_id = test_id)
	studentcount = students.count() 	
	scorecount = 0	
	for s in students:
		if s.score <= st.score:
			scorecount+=1
	percentile = round(float(scorecount)/float(studentcount)*100,2)	
	
	
	questions = StudentTestQA.objects.filter(student_test= st)
	result = []
	for q in questions:
		details ={}
		tq = testQuestion.objects.get(pk=int(q.question))
		details['question'] = tq.question
		if tq.correct_answer == q.answer:
			details['correct'] = True
		else:
			details['correct'] = False
			
		if tq.correct_answer == 'a':
			details['correct_answer'] = tq.option_a
		elif tq.correct_answer == 'b':
			details['correct_answer'] = tq.option_b
		elif tq.correct_answer == 'c':
			details['correct_answer'] = tq.option_c
		elif tq.correct_answer == 'd':
			details['correct_answer'] = tq.option_d
			
		if q.answer == 'a':
			details['user_answer'] = tq.option_a
		elif q.answer == 'b':
			details['user_answer'] = tq.option_b
		elif q.answer == 'c':
			details['user_answer'] = tq.option_c
		elif q.answer == 'd':
			details['user_answer'] = tq.option_d							

		result.append(details)
	return render_to_response('student-takentests.html', {'takenList':takenList,'result':result,'percentile':percentile} , context_instance=RequestContext(request))
	
	
def approved_tests(request):
	now = timezone.now()
	stests = StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),approved=True)
	testList = []
	for st in stests:
		if st.quiz.end_time > now:
			if st.taken == True:
				continue
			details = {}
			details['test_id'] = st.quiz.id
			details['client'] = st.quiz.client.userinfo.name
			details['title'] = st.quiz.title
			details['end_date'] = st.quiz.end_time
			details['duration'] = st.quiz.duration
			details['length'] = st.quiz.number_of_questions
			details['test_key'] = st.quiz.key
			testList.append(details)
	return testList
		
def student_dashboard(request):
	if request.user.groups.filter(name = 'Student').exists():
		return render_to_response('student-dashboard.html', {} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_dashboard_personal(request):		
	if request.user.groups.filter(name = 'Student').exists():
		return render_to_response('student-personal.html', {} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_dashboard_tests(request):		
	if request.user.groups.filter(name = 'Student').exists():
		return render_to_response('student-tests.html', {} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
		
def student_dashboard_opentests(request):		
	if request.user.groups.filter(name = 'Student').exists():
		openList = open_tests(request)
		return render_to_response('student-opentests.html', {'openList':openList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
		
def student_dashboard_closedtests(request):		
	if request.user.groups.filter(name = 'Student').exists():
		closedList = closed_tests(request)
		return render_to_response('student-closedtests.html', {'closedList':closedList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_dashboard_approvedtests(request):
	if request.user.groups.filter(name = 'Student').exists():
		approvedList = approved_tests(request)
		return render_to_response('student-approvedtests.html', {'approvedList':approvedList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_dashboard_ongoingtests(request):
	if request.user.groups.filter(name = 'Student').exists():
		ongoingList = ongoing_tests(request)
		return render_to_response('student-ongoingtests.html', {'ongoingList':ongoingList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_dashboard_appliedtests(request):
	if request.user.groups.filter(name = 'Student').exists():
		appliedList = applied_tests(request)
		return render_to_response('student-appliedtests.html', {'appliedList':appliedList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


		
def student_dashboard_takentests(request):
	if request.user.groups.filter(name = 'Student').exists():
		takenList = taken_tests(request)
		return render_to_response('student-takentests.html', {'takenList':takenList} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
		
		
def student_test(request,test_key):
	if request.user.groups.filter(name = 'Student').exists():
		t = quiz.objects.get(key=test_key)
		if t.type == '2' and	StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz=t,approved=False).count()>0:
			return HttpResponse('Your application hasnt been approved yet')
		details = {}
		if t.type == '2':
			details['approved'] = True
			
		if timezone.make_aware((t.start_time + datetime.timedelta(minutes=330)), timezone.get_default_timezone()) > timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()):
			details['not_yet'] = 1
			
		details['id']=t.id
		details['client'] = t.client.userinfo.name
		details['client_details'] = t.client.details
		details['title'] = t.title
		details['description'] = t.description
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		details['test_key'] = t.key
		return render_to_response('student-test.html', {'details':details} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def student_test_landing(request,test_key):
	if request.user.groups.filter(name = 'Student').exists():
		t = quiz.objects.get(key=test_key)
		details = {}
		details['id']=t.id
		details['client'] = t.client.userinfo.name
		details['title'] = t.title
#     details['description'] = t.description
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		details['test_key'] = t.key
		return render_to_response('student-test-landing.html', {'details':details} , context_instance=RequestContext(request))
		
	else:
		return HttpResponseRedirect('/')
def student_applytest(request,test_id):
	if request.user.groups.filter(name = 'Student').exists():
		t = quiz.objects.get(pk=test_id)	
		details = {}
		details['id']=t.id
		details['client'] = t.client.userinfo.name
		details['title'] = t.title
		details['end_date'] = t.end_time
		details['duration'] = t.duration
		details['length'] = t.number_of_questions
		x = simplejson.loads(t.applicationJSON)		
		details['no_q']= x['0']
		del x['0']
		details['apply_questions'] = x
		if StudentTest.objects.filter(student = student.objects.get(userinfo = userInfo.objects.get(user = request.user)),quiz = t).count() >0:
			details['applied'] = True
		else:
			details['applied'] = False
		
		return render_to_response('student-applytest.html', {'details':details} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
	
def student_bio(request):
	if request.user.groups.filter(name = 'Student').exists():
		details = {}
		user= request.user
		details['username'] = user.username
		details['name'] = userInfo.objects.get(user = user).name
		details['email'] = user.email
		details['college'] = student.objects.get(userinfo = userInfo.objects.get(user = user)).college
		details['year'] = student.objects.get(userinfo = userInfo.objects.get(user = user)).year
		details['department'] = student.objects.get(userinfo = userInfo.objects.get(user = user)).department
		return render_to_response('student-bio.html',{'details':details},context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def client_bio(request):
	if request.user.groups.filter(name = 'Client').exists():
		details = {}
		user= request.user
		details['username'] = user.username
		details['name'] = userInfo.objects.get(user = user).name
		details['email'] = user.email
		details['details'] = client.objects.get(userinfo = userInfo.objects.get(user = user)).details
		return render_to_response('client-bio.html',{'details':details},context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/')	

def client_dashboard_tests(request):
	if request.user.groups.filter(name = 'Client').exists():
		return render_to_response('client-tests.html', {} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def client_dashboard_student(request,student_id):
	if request.user.groups.filter(name = 'Client').exists():
		details = {}
		student_ = student.objects.get(pk = student_id)
		details['username'] = student_.userinfo.user.username
		details['name'] = student_.userinfo.name
		details['email'] = student_.userinfo.user.email
		details['college'] = student_.college
		details['year'] = student_.year
		details['department'] = student_.department
		return render_to_response('client-student.html',{'details':details},context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def client_dashboard(request):
	if request.user.groups.filter(name = 'Client').exists():
		return render_to_response('client-dashboard.html', {} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


def jqgrid_handler(request):
	page = int(request.GET['page'])
	limit = int(request.GET['rows'])
	sidx = str(request.GET['sidx'])
	sord = str(request.GET['sord'])
	if(sidx is None):
		sidx = 'id'
	count = quiz.objects.all().count()
	if count > 0:
		total_pages = ceil(count/limit)
	else:
		total_pages = 0
	
	start = limit*page - limit
	if sord == 'desc':
		temp = '-'
	else:
		temp = ''	
	# needs to be changed for client
	result = quiz.objects.filter(client = client.objects.get(userinfo = userInfo.objects.get(user = request.user))).order_by(temp+sidx)[start:start+limit]
	response = {}
	response['total'] = total_pages
	response['page'] = page
	response['records'] = count
	rows = []
	for r in result:
		temp = {}
		temp['id'] = r.id
		if r.type == '1':
			rtype = 'open'
		elif r.type == '2':
			rtype = 'closed'
		else:
			rtype = 'secret'
		temp['cell']=[r.id,r.title,r.duration,r.number_of_questions,rtype] 
		rows.append(temp)
	response['rows']=rows
	
	return HttpResponse(simplejson.dumps(response),content_type = "application/json")




def jqgrid_handler2(request):
	id = int(request.GET['ids'])
	
	page =int(request.GET['page'])
	limit =int(request.GET['rows'])
	sidx =str(request.GET['sidx'])
	sord = str(request.GET['sord'])
	if(sidx is None):
		sidx = 'id'
	count = StudentTest.objects.filter(quiz_id=id).count()
	if count > 0:
		total_pages = ceil(count/limit)
	else:
		total_pages = 0
	
	start = limit*page - limit
	if sord == 'desc':
		temp = '-'
	else:
		temp = ''	
	# needs to be changed for client
	result = StudentTest.objects.filter(quiz_id=id).order_by(temp+sidx)[start:start+limit]
	response = {}
	response['total'] = total_pages
	response['page'] = page
	response['records'] = count
	rows = []
	for r in result:
		temp = {}
		temp['id'] = r.id
		x1 = ''
		x2 =''
		if r.apply_datetime is not None:
			x1 = r.apply_datetime.strftime('%Y-%m-%d %X')
		else:
			x1 = '-'
		if r.test_datetime is not None:
			x2 = r.test_datetime.strftime('%Y-%m-%d %X')
		else:
			x2 = '-'
		
		application_questions = simplejson.loads(r.quiz.applicationJSON)
		try:
			application_answers = simplejson.loads(r.applicationJSON)
		except:
			application_answers = ''
		application_string = ''
		for i in range(1,int(application_questions['0'])+1):
			application_string =application_string + "<strong>" + str(application_questions[str(i)]) + "</strong>" +'<br/>'		
			application_string =application_string + str(application_answers[str(i)]) + '<br/>'
		student = "<a href='/client-dashboard/student/" + str(r.student.id) +"'>"+ r.student.userinfo.name + "</a>"
		temp['cell']=[r.id,student,x1,x2,application_string,r.approved,r.score] 
		rows.append(temp)
	response['rows']=rows
	
	return HttpResponse(simplejson.dumps(response),content_type = "application/json")







