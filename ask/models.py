from django.db import models
from django.contrib.auth.models import User
from djangosphinx.models import SphinxSearch

rating = models.IntegerField(default = 0)
rating.contribute_to_class(User, 'rating')
# Create your models here.
class Question(models.Model):
	header = models.CharField(max_length=400)
	body = models.TextField()
	user = models.ForeignKey(User)
	ask_date = models.DateTimeField()
	rating = models.IntegerField()
	search = SphinxSearch(
			weights = {
			'body' : 100,
			'header' : 90})
class Answer(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer_date = models.DateTimeField()
	content = models.TextField()
	isright = models.BooleanField()
	rating = models.IntegerField()
	search = SphinxSearch(
			weights = {
			'content' : 100})
class Likes(models.Model):
	type = models.IntegerField()
	user = models.ForeignKey(User)
	tid = models.IntegerField()
	action = models.IntegerField()
