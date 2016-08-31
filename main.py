import webapp2
import re

Signup_form= """
        <!DOCTYPE html>

        <html>
        <head>
            <title>Unit 2 Rot 13</title>
                <style type="text/css">
                .label {text-align: right}
                .error {color: red}
                </style>

                </head>

                <body>
                <h2>Signup</h2>
                <form method="post">
                <table>
                <tr>
                <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username"  value="%(username)s">
          </td>
           <td class="error" name="user_error">
             %(user_error)s
           </td>
           </tr>



        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password">
          </td>
          <td class="error" name="password_error">
            %(password_error)s
          </td>
          </tr>

          <tr>
          <td class="label">
            Verify Password
            </td>
          <td>
            <input type="password" name="verify">
          </td>
          <td class="error" name="verify_error">
            %(verify_error)s
          </td>
          </tr>

          <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s" >
          </td>
          <td class="error" name="email_error">
            %(email_error)s
          </td>

        </tr>
      </table>

      <input type="submit">
      </form>
      </body>

      </html>
      """
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
            e.g. www.Signup.com/
    """
    def write_form(self, username="", user_error="", password_error="", verify_error="", email="", email_error=""):
        self.response.write(Signup_form % {"username": username, "user_error": user_error, "password_error": password_error, "verify_error": verify_error, "email": email, "email_error": email_error})

    def get(self):
        self.write_form()
    def post(self):
        have_error = False
        username = self.request.get('username')
        user_error = self.request.get('user_error')
        password = self.request.get('password')
        password_error = self.request.get('password_error')
        verify = self.request.get('verify')
        verify_error = self.request.get('verify_error')
        email = self.request.get('email')
        email_error = self.request.get('email_error')

        if not valid_username(username):
            user_error="Please enter a valid user_name"
            have_error = True
        if not valid_password(password):
            password_error="Please enter a valid password"
            have_error = True
        if not verify==password:
            verify_error= "Password doesnot match"
            have_error = True
        if email:
            if not valid_email(email):
                email_error="Please enter a valid email "
                have_error = True
        if have_error:
            self.write_form(username, user_error, password_error, email, email_error)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
         username = self.request.get('username')
         self.response.write("Welcome "+username)
app = webapp2.WSGIApplication([
                               ('/', Signup),
                               ('/welcome',Welcome)],
                              debug=True)
