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

form="""
<form method="post" action="/">
    <textarea name="text" rows="4" cols="50">%(text)s</textarea><br>
  <input type="submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)
	
def rot13(s):
	a = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
		 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
	r = ('n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm')
	d = dict(zip(a,r))
	
	newstring = ''
	for l in s:
		if l.lower() in d:
			if l.isupper() == True:
				newstring += d[l.lower()].upper()
			else:
				newstring += d[l]
		else:
			newstring += l
	return newstring

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.write_form()
	def post(self):
		user_text = self.request.get('text')
		self.write_form(escape_html(rot13(user_text)))
	def write_form(self,text=""):
		self.response.out.write(form%{"text":text})

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
