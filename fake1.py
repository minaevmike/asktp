import MySQLdb as db
import random
import string
import datetime
from random import randint
def id_generator(size=6,chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for x in range(size))
con=db.connect(host="localhost",user="ask_user",passwd="1",db="ask_db1")
cur=con.cursor()
x = 0
while ( x < 100000):
	if (x % 1000 == 0):
		print x
	x = x + 1
	try:
		cur_date = datetime.datetime.now()
		cur_date = str(cur_date)
		h = id_generator(randint(20,40),string.ascii_lowercase + " ")
		b = id_generator(randint(50,400),string.ascii_lowercase + " ")
		u = randint(1,10000)
		cur.execute("""INSERT INTO `ask_question` (`header`,`body`,`user_id`,`ask_date`,`rating`) VALUES (%s,%s,%s,%s,%s)""",(h,b,u,cur_date, str(0)))
	except:
		con.commit()
		print u
con.commit()
