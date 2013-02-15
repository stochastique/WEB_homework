#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
  
def valid_password(password):
    return PASS_RE.match(password)
	
def valid_email(email):
    return MAIL_RE.match(email)

form="""
<form method="post" action="/">
    <input type="text" name="username" value="%(username)s">%(error1)s<br>
	<input type="password" name="password" value="%(password)s">%(error2)s<br>
	<input type="password" name="verify" value="%(verify)s">%(error3)s<br>
	<input type="text" name="email" value="%(email)s">%(error4)s<br>
	<input type="submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.write_form()
	def post(self):
		user_username = self.request.get('username')
		user_password = self.request.get('password')
		user_verify   = self.request.get('verify')
		user_email    = self.request.get('email')
		
		if (valid_username(user_username) and valid_password(user_password) and
			valid_password(user_verify) and (user_password == user_verify) and 
			valid_email(user_email)):
			self.redirect("/welcome?username=%(username)s" %{"username":user_username})
		elif (valid_username(user_username) and valid_password(user_password) and
			  valid_password(user_verify) and (user_password == user_verify) and
			  (not user_email)):
			  self.redirect("/welcome?username=%(username)s" %{"username":user_username})
		else:
			error1 = (not valid_username(user_username))*"That's not a valid username."
			error2 = (not valid_password(user_password))*"That wasn't a valid password."
			error3 = bool(valid_password(user_password))*(user_password != user_verify)*"Your passwords didn't match."
			error4 = bool(user_email)*(not valid_email(user_email))*"That's not a valid email."
			self.write_form(escape_html(user_username),"","",escape_html(user_email),
							error1,error2,error3,error4)
		
	def write_form(self,username="",password="",verify="",email="",
				   error1="",error2="",error3="",error4=""):
		self.response.out.write(form%{"username":username,
									  "password":password,
									  "verify":verify,
									  "email":email,
									  "error1":error1,
									  "error2":error2,
									  "error3":error3,
									  "error4":error4})
									  
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome, "+self.request.get('username')+"!")

app = webapp2.WSGIApplication([('/', MainHandler),
							   ('/welcome', WelcomeHandler)],
                              debug=True)
