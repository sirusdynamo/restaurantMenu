from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi


#importing CRUD operations to obatain data from database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,MenuItem,Restaurant

engine= create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine

DBSession=sessionmaker(bind=engine)
session=DBSession()

# please note that
# output=output.encode()
# by default encodes to "UTF-8" standard
# Hence the reason for the dedcode  in do_POST  function



class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output=""
                output+="<html><body>"
                output+="Hello"
                output+="<form method='POST' action='/hello' enctype='multipart/form-data'>"
                output+="<h1>what would you like to say back</h1>"
                output+="<input type='text' name='message' id='message'>"
                output+="<input type='submit' value='Submit'>"
                output+="</form></body></html>"
                output=output.encode()
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<form action='/restaurant/new' method='POST' enctype='multipart/form-data'>"
                output+="""<label>Enter restaurant name:
                            <input type=text name=newRestaurant id=newRestaurant placeholder=''>
                            </label>
                            <input type='submit' value='Submit'>
                            """
                output+="</body></html>"
                output=output.encode()
                self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                restaurants= session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output=""
                output+="<a href='/restaurant/new'>Make a new restaurant</a>"
                output+="<html><body>"
                for restaurant in restaurants:
                    output+=restaurant.name
                    output+="<br>"
                    output+="<a href='/restaurants/%s/edit'>Edit</a>" %restaurant.id
                    output+="<br>"
                    output+="<a href='/restaurants/%s/delete'>Delete</a>"%restaurant.id
                    output+="<br>"

                output+="</body></html>"
                output=output.encode()
                self.wfile.write(output)

                return
            
            # if self.path.endswith("/delete"):

            if self.path.endswith("/edit"):
                restaurant_id_path=self.path.split("/")[2]
                my_restaurant_query=session.query(Restaurant).filter_by(id=restaurant_id_path).one()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output+=""
                output+="<html><body>"
                output+="<form action='/restaurants/%s/edit' method='POST' enctype='multipart/form-data'>"%restaurant_id_path
                output+="<input type='text' name='newRestaurantName' placeholder='%s'>"%my_restaurant_query.name
                output+="<input type='submit' value='Rename'>"
                output+="</body></html>"
                output=output.encode()
                self.wfile.write(output)
                return




            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()


                output=""
                output+="<html><body>   Hola   <a href='/hello'>hello</a></body></html>"
                output=output.encode()
                self.wfile.write(output)
                print(output)
                return


        except IOError:
            self.send_error(404,"File not found %s" %self.path)



    def do_POST(self):
        try:
            if self.path.endswith("/restaurant/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                redirect_path='/restaurants'
                self.send_header('Location',redirect_path)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')[0].decode('utf-8')#


                #create a new restaurant class
                newRestaurant=Restaurant(name=messagecontent)
                session.add(newRestaurant)
                session.commit()

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype,pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary']=bytes(pdict['boundary'],'utf-8')
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent =fields.get()[0].decode('utf-8')
                #obtain restaurant id

                restaurant_id_path=self.path.split("/")[2]
                my_restaurant_query=session.query(Restaurant).filter_by(id=restaurant_id_path).one()
                if my_restaurant_query!=[]:
                    my_restaurant_query.name=messagecontent
                    session.add(my_restaurant_query)
                    session.commit()





            
            




        #     self.send_response(301)
        #     self.end_headers()

        #     ctype,pdict=cgi.parse_header(self.headers.getheader('Content-type'))
        #     if ctype=='multipart/form-data':
        #         fields=cgi.parse_multipart(self.rfile,pdict)
        #         messagecontent=fields.get('message')
        #     output=""
        #     output+="<html><body>"
        #     output+="<h2>whats been said %s</h2>" % messagecontent[0]



        #     output+="""<form method='POST' enctype='multipart/form-data' action='/hello'> 
        #     <h1>what would you like to say </h1><input type='text' name='message'>
        #     <input type='submit' value='Submit'>
        #     </form></body></html>"""
        #     outpout=output.encode()
        #     self.wfile.write(output)
        #     print(output)
        #     return
        


#*********************************************************************
#     """
#             self.send_response(301)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
#             if ctype == 'multipart/form-data':
#                 pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 messagecontent = fields.get('message')[0].decode('utf-8')
#             output = ''
#             output += '<html><body>'
#             output += '<h2> Okay, how about this: </h2>'
#             output += '<h1> %s </h1>' % messagecontent
#             output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
#             output += '</html></body>'
#             self.wfile.write(output.encode('utf-8'))
# """*******************************************************************************
            
            # # Doesn't do anything with posted data
            # content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            # post_data = self.rfile.read(content_length) # <--- Gets the data itself
            # print (post_data) # <-- Print post data
            # self.wfile.write(post_data)
            # self._set_headers()


            # #######################################################################
            # content_length = int(self.headers['Content-Length'])
            # body = self.rfile.read(content_length)
            # self.send_response(200)
            # self.end_headers()
            # response = BytesIO()
            # response.write(b'This is POST request. ')
            # response.write(b'Received: ')
            # response.write(body)
            # self.wfile.write(response.getvalue())



        except:

            pass
def main():
    try:
        server_port=8080
        server_name=''
        server_address=(server_name,server_port)
        server=HTTPServer(server_address,webserverHandler)
        print("web server running on port {}".format(server_port))

        server.serve_forever()
    except KeyboardInterrupt :
        print(" ^c entered server is closing")
        server.socket.close()


if __name__ == '__main__':
    main()
