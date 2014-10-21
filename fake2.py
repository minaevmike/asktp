import MySQLdb as db
import random
import string
import datetime
import sys
from random import randint
def id_generator(size=6,chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for x in range(size))
con=db.connect(host="localhost",user="ask_user",passwd="1",db="ask_db1")
cur=con.cursor()
x = 0
while ( x < 2000000):
	try:
		if(x % 10000 == 0):
			print x
		x = x + 1
		cur_date = datetime.datetime.now()
		cur_date = str(cur_date)
		a_id = randint(1,10000)
		q_id = randint(1,100000)
		text = id_generator(randint(50,1000),string.ascii_uppercase + string.digits + string.ascii_lowercase + " ")
		ch = random.choice((True, False))
		cur.execute("""INSERT INTO `ask_answer` (`author_id`,`question_id`,`answer_date`,`content`,`isright`,`rating`) VALUES (%s,%s,%s,%s,%s,%s)""",(a_id,q_id,cur_date,text,ch,str(0)))
	except:
		con.commit()
		print(a_id)
		print(q_id)
con.commit()
