import os.path
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options

define("port", default=8778, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="myticket", help="database name")
define("mysql_user", default="g", help="database user")
define("mysql_password", default="z", help="database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # GET METHOD :
            (r"/signup/([^/]+)/([^/]+)", signup),
            (r"/login/([^/]+)/([^/]+)", login),
            (r"/logout/([^/]+)/([^/]+)", logout),
            (r"/sendticket/([^/]+)/([^/]+)/([^/]+)", sendticket),
            (r"/getticketcli/([^/]+)", getticketcli),
            (r"/closeticket/([^/]+)/([^/]+)", closeticket),
            (r"/getticketmod/([^/]+)", getticketmod),
            (r"/restoticketmod/([^/]+)/([^/]+)/([^/]+)", restoticketmod),
            (r"/changestatus/([^/]+)/([^/]+)/([^/]+)", changestatus),
            # POST METHOD :
            (r"/signup", signup),
            (r"/login", login),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/getticketcli", getticketcli),
            (r"/closeticket", closeticket),
            (r"/getticketmod", getticketmod),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),

        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

#________________________________________________________________________________________________

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def check_user(self, user):
        resuser = self.db.get("SELECT * from users where username = %s", user)
        if resuser:
            return True
        else:
            return False

    def check_token(self,token):
        resuser = self.db.get("SELECT * from users where token = %s", token)
        if resuser:
            return True
        else:
            return False
    def check_auth(self, username, password, role):
        resuser = self.db.get("SELECT * from users where username = %s and password = %s and role = %s", username, password , role)
        if resuser:
            return True
        else:
            return False
    def check_admin(self,token):
        myrole = self.db.get("SELECT role from users where token =%s ", token)
        if {'role': 'Admin'}:
            return True
        else:
            return False
#__________________________________________________________________________________________________----
class defaulthandler(BaseHandler):
    def post(self, *args, **kwargs):
        output = {'status': 'Wrong Command'}
        self.write(output)

#------------------------------------------------------------------------------------------------

class signup(BaseHandler):
    def get(self, *args):
        if not self.check_user(args[0]):
            api_token = str(hexlify(os.urandom(8)))
            user_id = self.db.execute("INSERT INTO users (username, password,role ,token) "
                                      "VALUES (%s,%s,%s,%s) "
                                      , (args[0], args[1], args[6], api_token))
            output = {"message": "Signed Up Successfully",
                      "code": "200"}
            self.write(output)
        else:
            output = {"message": 'this username already exits'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        role = self.get_argument('role')
        if not self.check_user(username):
            api_token = str(hexlify(os.urandom(8)))
            user_id = self.db.execute("INSERT INTO users (token,username, password,role) "
                                     "values (%s,%s,%s,%s) "
                                     ,api_token ,username, password,role)

            output = { "message": "Signed Up Successfully",
                        "code" : "200"}

            self.write(output)
        else:
            output = {"message": 'this username already exits'}
            self.write(output)

#--------------------------------------------------------------------------------------------

class login(BaseHandler):
    def get(self,*args):
        if self.check_auth(args[0], args[1], args[6]):
            user = self.db.get("SELECT * from users where username = %s and password = %s and role=%s", args[0],args[1], args[6])
            output = { "message": "Logged in Successfully",
                       "code": "200",
                       'token': user.token}
            self.write(output)
        else:
            output = {"message": 'Can not login, Wrong Authentication'}
            self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        role = self.get_argument('role')
        if self.check_auth(username,password,role):
            user = self.db.get("SELECT * from users where username = %s and password = %s and role= %s ", username,password, role)
            output = { "message": "Logged in Successfully",
                       "code": "200",
                       'token': user.token}
            self.write(output)
        else:
            output = {"message": 'Can not login, Wrong Authentication'}
            self.write(output)
#--------------------------------------------------------------------------------------
class logout(BaseHandler):
    def get(self,*args):
        if self.check_auth(args[0], args[1] ,args[6]):
            user = self.db.get("SELECT * from users where username = %s and password = %s and role= %s ", args[0],args[1] , args[6])
            output = { "message": "Logged out Successfully",
                       "code": "200"}
            self.write(output)
        else:
            output = {"message": 'Wrong Authentication'}
            self.write(output)

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        role = self.get_argument('role')
        if self.check_auth(username, password,role):
            user = self.db.get("SELECT * from users where username = %s and password = %s and role = %s", username,password,role)
            output = { "message": "Logged out Successfully",
                       "code": "200"}
            self.write(output)
        else :
            output = {"message": 'Wrong Authentication'}
            self.write(output)
#---------------------------------------------------------------------------------------------

class sendticket(BaseHandler):
    def get(self, *args):
        if self.check_token(args[0]):
            ticket = self.db.execute("INSERT INTO tickets (token, subject, body, status) "
                                      "values (%s,%s,%s,%s) "
                                      , (args[0], args[1], args[2], "Open"))
            ticket = self.db.get("SELECT * from tickets where token = %s and body = %s", args[0], args[2])
            output = {"message": "Ticket Sent Successfully",
                      "id": ticket.id,
                      "code": "200"}

            self.write(output)
        else:
            output = {"message": 'Wrong Token'}
            self.write(output)

    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        if self.check_token(token):
            ticket = self.db.execute("INSERT INTO tickets (body, subject, status, token) "
                                     "values (%s,%s,%s,%s) "
                                     , body, subject,"Open", token)
            #ticket = self.db.get("SELECT * from tickets where token = %s and body = %s", token, body)
            output = {"message": "Ticket Sent Successfully",
                      #"id": ticket.id,
                      "code": "200"}

            self.write(output)
        else:
            output = {"message": 'Wrong Token'}
            self.write(output)
#----------------------------------------------------------------------------
#ask
class getticketcli(BaseHandler):
    def get(self,*args):
        if self.check_token(args[0]):
            ticket = self.db.execute("SELECT * from tickets where token = %s", (args[0],))
            myfetch = self.db.fetchall()
            output = { "code": "200" }
            temp = "block "
            i = 0
            for arr in myfetch:
                output[temp + str(i)] = { "subject": arr[2],
                                          "body": arr[3],
                                          "status": arr[4],
                                          "id": arr[0],
                                          "reply": arr[5]}
                i += 1
            output["tickets"] = str(i)

            self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        if self.check_token(token):
            ticket = self.db.execute("SELECT * from tickets where token = %s", token)
            output = { "code": "200" }
            temp = "block "
            i = 0
            for arr in ticket:
                output[temp + str(i)] = { "subject": arr[2],
                                          "body": arr[3],
                                          "status": arr[4],
                                          "id": arr[0],
                                          "reply": arr[5]}
                i+=1
            output["tickets"] = str(i)

            self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

#---------------------------------------------------------------------------------
#edite
class closeticket(BaseHandler):
    def get(self,*args):
        if self.check_token(args[0]) and self.check_admin(args[0],args[1]):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(args[1]))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set status = %s where ticket_id = %s", ("close", int(args[1])))
                output = {    "message": "Ticket closed Successfully",
                              "code": "200" }

                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('ticket_id')
        if self.check_token(token):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(ticket_id))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set status = %s where ticket_id = %s", "close", int(ticket_id))
                output = {    "message": "Ticket closed Successfully",
                              "code": "200" }

                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

#----------------------------------------------------------------------------------------
#edite needed
class getticketmod(BaseHandler):
    def get(self,*args):
        if self.check_admin(args[0], args[1]):
            ticket = self.db.execute("SELECT * from tickets")
            myfetch = self.db.fetchall()
            output = { "code": "200" }
            temp = "block "
            i = 0
            for arr in myfetch:
                output[temp + str(i)] = { "subject": arr[2],
                                          "body": arr[3],
                                          "status": arr[4],
                                          "id": arr[0],
                                          "reply": arr[5]}
                i+=1
            output["tickets"] = str(i)

            self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        if self.check_admin(token):
            ticket = self.db.execute("SELECT * from tickets")
            output = { "code": "200" }
            temp = "block "
            i = 0
            for arr in ticket:
                output[temp + str(i)] = { "subject": arr[2],
                                          "body": arr[3],
                                          "status": arr[4],
                                          "id": arr[0],
                                          "reply": arr[5]}
                i+=1
            output["tickets"] = str(i)

            self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

#----------------------------------------------------------------

class restoticketmod(BaseHandler):
    def get(self,*args):
        if self.check_admin(args[0],args[1]):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(args[1]))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set response = %s where ticket_id = %s", (args[2], int(args[1])))
                output = {    "message": "Response to Ticket Sent Successfully",
                              "code": "200" }
                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

    def post(self, *args, **kwargs):
        response = self.get_argument('response')
        token = self.get_argument('token')
        ticket_id = self.get_argument('ticket_id')
        if self.check_admin(token):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(ticket_id))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set response = %s where ticket_id = %s", response, int(ticket_id))
                output = {    "message": "Response to Ticket Sent Successfully",
                              "code": "200" }
                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

#----------------------------------------------------------------------------

class changestatus(BaseHandler):
    def get(self,*args):
        if self.check_admin(args[0],args[1]):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(args[1]))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set status = %s where ticket_id = %s", (args[2], int(args[1])))
                output = {    "message": "Status Ticket Changed Successfully",
                              "code": "200" }
                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)
    def post(self, *args, **kwargs):
        token = self.get_argument('token')
        ticket_id = self.get_argument('ticket_id')
        body = self.get_argument('status')
        if self.check_admin(token):
            ticket = self.db.get("SELECT * from tickets where ticket_id = %s", int(ticket_id))
            if ticket:
                ticket = self.db.execute("UPDATE tickets set status = %s where ticket_id = %s", body, int(ticket_id))
                output = {    "message": "Status Ticket Changed Successfully",
                              "code": "200" }
                self.write(output)
            else:
                output = {"message":'Wrong id'}
                self.write(output)
        else :
            output = {"message":'Wrong Token'}
            self.write(output)

#-----------------------------------------------------------------------------

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
