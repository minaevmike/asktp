from django.shortcuts import render, render_to_response
from ask.models import User, Question, Answer, Likes
from django.views.generic import ListView, DetailView
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ask.form import AskForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError 
from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):
	def __init__(self, subject, html_content, rcpt):
		self.subject = subject
		self.rcpt = rcpt
		self.html_content = html_content
		threading.Thread.__init__(self)
	
	def run (self):
		msg = EmailMessage(self.subject, self.html_content, to = self.rcpt)
		msg.send()

def send_email(subject, html_content, rcpt):
	EmailThread(subject, html_content, rcpt).start()

def erquestion(request, errors, success = []):
	prev_page = None
	next_page = None
	paginate_by = 20
	try:
		p = 1
		ask_form = AskForm() 
		question = Question.objects.all().order_by('-ask_date')
		paginator = Paginator(question, paginate_by)
		latest_question = paginator.page(p)
		u = User.objects.all().order_by('-date_joined')[:10]
	except PageNotAnInteger:
		contacts = paginator.page(1)
		errors.append("Wrong page number")
	except EmptyPage:
		contacts = paginator.page(1)
		errors.append("Empty page")
	except:
		errors.append("Something goes wrong")
	return render(request, 'ask/question.html', { 'latest_question':latest_question,'AskForm':ask_form, 'errors':errors,'last_users':u })

def search(request):
	errors = []
	ask_form = AskForm()
	try:
		p = request.GET.get('q','')
		if (p == ''):
			errors.append("No search query")
			return erquestion(request,errors)
		q = list(Question.search.query(p))
		u = User.objects.all().order_by('-date_joined')[:10]
		return  render(request, 'ask/question.html', {'latest_question':q, 'AskForm':ask_form, 'last_users':u})
	except:
		errors.append("Uknown error")
		return erquestion(request, errors)

def index(request):
	errors = []
	prev_page = None
	next_page = None
	paginate_by = 20
	try:
		p = request.GET.get('page', '1')
		ask_form = AskForm() 
		question = Question.objects.all().order_by('-ask_date')
		paginator = Paginator(question, paginate_by)
		latest_question = paginator.page(p)
		u = User.objects.all().order_by('-date_joined')[:10]
	except PageNotAnInteger:
		contacts = paginator.page(1)
		errors.append("Wrong page number")
	except EmptyPage:
		contacts = paginator.page(1)
		errors.append("Empty page")
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return render(request, 'ask/question.html', { 'latest_question':latest_question,'AskForm':ask_form, 'errors':errors,'last_users':u })

def popular(request):
	q = Question.objects.all().order_by('-rating')[:20]
	ask_form = AskForm() 
	return render(request, 'ask/question.html', { 'latest_question':latest_question,'AskForm':ask_form })

def like(request):
	errors =[]
	if not request.user.is_authenticated():
		errors.append("You need to login")
		return erquestion(request, errors)
	try:
		q_id = request.GET['id']
		p = Question.objects.get(pk=q_id)
		l, created = Likes.objects.get_or_create(type = 1, user = request.user, tid = q_id, defaults={'type':1, 'user':request.user,'action': 0, 'tid':q_id})
		if (l.action == -1):
			l.action = 0
		if (l.action == 1):
			errors.append("You can't vote twice")
			return erquestion(request, errors)
		l.action += 1
		l.save()
		u = p.user
		u.rating += 3
		p.rating += 1
		p.save()
		u.save()
	except Question.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return HttpResponseRedirect("/")

def dislike(request):
	errors = []
	if not request.user.is_authenticated():
		errors.append("You need to login")
		return erquestion(request, errors)
	try:
		q_id = request.GET['id']
		p = Question.objects.get(pk=q_id)
		l, created = Likes.objects.get_or_create(type = 1, user = request.user, tid = q_id, defaults={'type':1, 'user':request.user,'action': 0, 'tid':q_id})
		if (l.action == 1):
			l.action = 0
		if (l.action == -1):
			errors.append("You can't vote twice")
			return erquestion(request, errors)
		l.action -= 1
		l.save()
		u = p.user
		u.rating -= 2
		u.save()
		p.rating -= 1
		p.save()
	except Question.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return HttpResponseRedirect("/")

def alike(request):
	errors = []
	if not request.user.is_authenticated():
		errors.append("You need to login")
		return erquestion(request, errors)
	try:
		q_id = request.GET['id']
		p = Answer.objects.get(pk=q_id)
		l, created = Likes.objects.get_or_create(type = 2, user = request.user, tid = q_id, defaults={'type':2, 'user':request.user,'action': 0, 'tid':q_id})
		if (l.action == -1):
			l.action = 0
		if (l.action == 1):
			errors.append("You can't vote twice")
			return erquestion(request, errors)
		l.action += 1
		l.save()
		p.rating += 1
		u = p.author
		u.rating += 5
		u.save()
		p.save()
	except Answer.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return HttpResponseRedirect("/answers/?id=" + str(p.question.id))

def adislike(request):
	errors = []
	if not request.user.is_authenticated():
		errors.append("You need to login")
		return erquestion(request, errors)
	try:
		q_id = request.GET['id']
		p = Answer.objects.get(pk=q_id)
		l, created = Likes.objects.get_or_create(type = 2, user = request.user, tid = q_id, defaults={'type':2, 'user':request.user,'action': 0, 'tid':q_id})
		if (l.action == 1):
			l.action = 0
		if (l.action == -1):
			errors.append("You can't vote twice")
			return erquestion(request, errors)
		l.action -= 1
		l.save()
		p.rating -= 1
		u = p.author
		u.rating -= 2
		u.save()
		p.save()
	except Answer.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return HttpResponseRedirect("/answers/?id=" + str(p.question.id))

def answers(request):
	errors = []
	ask_form = AskForm()
	answer_form = AnswerForm()
	q = None
	a = None
	try:
		q_id = request.GET['id']
		q = Question.objects.get(pk=q_id)
		a = Answer.objects.filter(question=q_id)
		u = User.objects.all().order_by('-date_joined')[:10]
	except Question.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except Answer.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return render(request, 'ask/answers.html', { 'question':q, 'answers':a , 'AskForm':ask_form,'errors':errors,'AnswerForm':answer_form,'last_users':u })

@csrf_exempt
def register(request):
	errors = []
	try:
		username = request.POST['name']
		password = request.POST['password']
		email = request.POST['mail']
		if (email.find('@') == -1):
			errors.append('Wrong email')
			return erquestion(request, errors)
		user=User.objects.create_user(username=username, password=password,email=email)
		user.save()
		send_email('Nice, you register %s' % (username), ' username - %s \n password - %s' % (username, password), [email])
		return HttpResponseRedirect('/')
	except IntegrityError:
		errors.append("User with this nick already registrated")
		return erquestion(request, errors)
	except :
		errors.append("Uknown error")
		return erquestion(request, errors)

	
@csrf_exempt
def ask(request):
	errors = []
	if not request.user.is_authenticated():
		errors.append("you need to login !!")
		return erquestion(request, errors)
	else:
		if request.method == 'POST':
			form = AskForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				u = request.user
				he = cd['header']
				b = cd['body']
				q = Question(header = he, body = b, user = u, ask_date = timezone.now(), rating = 0)
				q.save()
				send_email('Nice, your question was published, %s' % (u.username), '%s \n %s' %(he, b), [u.email])
				u = User.objects.all().order_by('-date_joined')[:10]
				return HttpResponseRedirect("/")
			else:
				errors.append("All feilds in ask form are required")
				return erquestion(request, errors)
	latest_question = Question.objects.all().order_by('-ask_date')[:20]
	ask_form = AskForm()
	return render(request, 'ask/question.html', { 'errors':errors , 'latest_question':latest_question , 'AskForm':ask_form, 'last_users':u })

@csrf_exempt
def ans(request):
	errors =[]
	if not request.user.is_authenticated():
		errors.append("You need to login")
		return erquestion(request, errors)
	else:
		try:
			q_id = request.GET['id']
			if request.method == 'POST':
				form = AnswerForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					u = request.user
					q = Question.objects.get(id = q_id)
					a = Answer(author = u, question = q, answer_date = timezone.now(), content = cd['content'], isright = False, rating = 0)
					a.save()
					body = cd['content']
					send_email('%s answer to your question, %s' % (u.username , q.user.username),  body, [q.user.email])
					return HttpResponseRedirect("/answers/?id=" + str(q_id))
		except Question.DoesNotExist:
			errors.append("Wrong id")
			return erquestion(request, errors)
		except KeyError:
			errors.append("No id field in get request")
			return erquestion(request, errors)
		except:
			errors.append("Something goes wrong")
			return erquestion(request, errors)
	return HttpResponseRedirect("/answers/?id=" + str(q_id))

def user(request):
	errors = []
	l_question = []
	l_answer = []
	try:
		u_id = request.GET['id']
		u = User.objects.get(id = u_id)
		if (u):
			l_question = Question.objects.filter(user = u).order_by('-ask_date')[:10]
			l_answer = Answer.objects.filter(author = u).order_by('-answer_date')[:10]
		ask_form = AskForm()
		us = User.objects.all().order_by('-date_joined')[:10]
		return render(request, 'ask/user.html', {  'AskForm':ask_form, 'user_i':u, 'l_question':l_question, 'l_answer':l_answer, 'last_users':us })
	except KeyError:
		errors.append("Wrond id format")
		return erquestion(request, errors)
	except:
		errors.append("Uknown error")
		return erquestion(request, errors)

def righta(request):
	errors = []
	try:
		a_id = request.GET['id']
		a = Answer.objects.get(id = a_id)
		a.isright = True
		a.save()
		return HttpResponseRedirect("/answers/?id=" + str(a.question.id))
	except KeyError:
		errors.append("Wrong id format")
		return erquestion(request, errors)
	except:
		errors.append("Uknown error")
		return erquestion(request, errors)

def answer(request):
	errors = []
	try:
		q_id = request.GET['id']
		q = Question.objects.get(pk = q_id)
		ask_form = AskForm()
		answer_form = AnswerForm()
		u = User.objects.all().order_by('-date_joined')[:10]
	except Question.DoesNotExist:
		errors.append("Wrong id")
		return erquestion(request, errors)
	except KeyError:
		errors.append("No id field in get request")
		return erquestion(request, errors)
	except:
		errors.append("Something goes wrong")
		return erquestion(request, errors)
	return render(request, 'ask/answer.html', { 'errors':errors , 'question':q, 'AnswerForm':answer_form , 'AskForm':ask_form,'last_users':u })

@csrf_exempt
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/")

@csrf_exempt
def login_user(request):
	logout(request)
	errors = []
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None and user.is_active:
		login(request, user)
		return HttpResponseRedirect("/")
	else:
		errors.append("Wrong username or password")
		return erquestion(request, errors)
# Create your views here.
