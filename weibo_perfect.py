#coding=utf-8
import weibo
import time
from flask import Flask, request, render_template, redirect, url_for
from random import choice
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

APP_KEY = "977462038"
APP_SECRET = 'b2abc8e87fee95ad3a6acf7b7c92409a'
CALLBACK = 'http://127.0.0.1:5000/aaa'

comment_list = ['抢占头条','坐沙发','前排','抢沙发','前排围观','火钳刘明']
app = Flask(__name__)
@app.route('/')
def get_code():
	return render_template('weibo.html')
@app.route('/aaa', methods=['GET'])
def run():
	client = weibo.APIClient(APP_KEY,APP_SECRET,CALLBACK)
	auth_url = client.get_authorize_url()
	code = request.args.get('code').encode("utf-8")
	print "get code!"
	r = client.request_access_token(code)
	client.set_access_token(r.access_token,r.expires_in)
	comment_old = 0
	mid_pool = []
	while True:
		weibo_nr= client.statuses.friends_timeline.get(count="50")
		for x in weibo_nr["statuses"]:
			#if x["user"]["id"] == 3200361441:
			if x["user"]["id"] ==2642757171:
				
				if len(mid_pool) == 0:
					mid_pool.append(x["mid"])
					break
				else:
					mid_target = x["mid"]
					print  "x[mid] = "+str(mid_target)
					if mid_target in mid_pool:
						print "nothing happend"
						break
					else:
						print "get new weibo!!"
						comment = choice(comment_list)
						while comment_old==comment:
							comment = choice(comment_list)
						client.comments.create.post(comment=comment,id=mid_target)
						print "success!! mid = "+str(mid_target)
						mid_pool.append(mid_target)
						comment_old = comment
						break
				print "search already done"
			else:
				print "He's not the target"
		time.sleep(4)
	return "Done"
if __name__ == "__main__":
	app.run(debug=True)
