import MySQLdb as db
import random
import string
import datetime
from random import randint
from django.contrib.auth.models import User
def id_generator(size=6,chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for x in range(size))
x = 0
while ( x < 10000):
	if (x % 500 == 0):
		print x
	x = x + 1
	uname = id_generator(randint(6,12))
	pas = id_generator(randint(8,16))
	mail = id_generator(randint(6,12)) + "@" + id_generator(randint(6,12),string.ascii_lowercase)+"."+id_generator(randint(2,3),string.ascii_lowercase)
	user=User.objects.create_user(username=uname, password=pas,email=mail)
	user.save()
