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

signup_form="""
<html>
    <head>
        <title>User Sign Up</title>
    </head>

    <body>
        <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error" style = "color:red">%(error_name)s %(error_noname)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error" style = "color:red">%(error_pwd)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="cpwd">Confirm Password</label></td>
                    <td>
                        <input name="cpwd" type="password" required>
                        <span class="error" style = "color:red">%(error_cpwd)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error" style = "color:red">%(error_email)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_name="", error_noname="", error_pwd="", error_cpwd="", error_email="", username="", email=""):
        self.response.out.write(signup_form %{"error_name": error_name, "error_noname": error_noname, "error_pwd": error_pwd, "error_cpwd": error_cpwd, "error_email": error_email, "username": username, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        global username
        username = self.request.get('username')
        password = self.request.get('password')
        cpwd = self.request.get('cpwd')
        email = self.request.get('email')

        name = valid_username(username)
        pwd = valid_password(password)
        em = valid_email(email)

        #errname_escaped = ""
        #errpwd_escaped = ""
        #errorcpwd_escaped = ""
        #erroremail_escaped = ""

        error_name = ""
        error_pwd = ""
        error_cpwd = ""
        error_email = ""
        error_noname = ""

        if not name:
            error_name = "Username is not valid.".format(username)
            #errname_escaped =cgi.escape(error_name, quote=True)

        if username == "":
            error_noname = "Username is blank. Please choose a username.".format(username)
            #errname_escaped = cgi.escape(error_noname, quote=True)

        if not pwd:
            error_pwd = "Please enter a password.".format(password)
            #errpwd_escaped = cgi.escape(error_pwd, quote=True)

        if password != cpwd:
            error_cpwd = "Passwords do not match.".format(cpwd)
            #errorcpwd_escaped = cgi.escape(error_cpwd, quote=True)

        if not em:
            error_email = "Email is not valid, please enter a valid email.".format(email)
            #erroremail_escaped = cgi.escape(error_email, quote=True)

        #self.write_form(errname_escaped, errpwd_escaped, errorcpwd_escaped, erroremail_escaped, username, email)
        self.write_form(error_name, error_noname, error_pwd, error_cpwd, error_email)

        if(name and pwd and em and (password == cpwd)):
            self.redirect("/welcome")

class Welcome(MainHandler):

    def get(self):

        response = "<h1>" "Welcome " + username + "!" "</h1>"
        #response = welcome
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
