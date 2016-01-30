# ---------------------------------------------------------------------
# filename : core.py
# contains code for all functonalities of the app
# creator : ajay
# date : 28 nov 2015
# version 1.0
#----------------------------------------------------------------------

from flask import Flask, render_template, request, redirect,jsonify, url_for, flash,Response
from sqlalchemy import create_engine,asc
from sqlalchemy.orm import sessionmaker
from database_setup import Genre, Base, Albums,User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import httplib2
import json
from flask import make_response
import requests
import dicttoxml
import uuid

# client id from google
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
app = Flask(__name__)

# dependecies to store images for items 
from werkzeug import secure_filename
UPLOAD_FOLDER = '/vagrant/item-catalog/static/cover_art'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Connect to Database and create database session
engine = create_engine('sqlite:///music_store.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/home/')
# ''' 
#     # renders the home template along with the list of geners 
#     # args  None
    
#     # returns  
#     # genre : curser of genre from database
#     # logout :if the user session exists( boolean )
# ''' 
def home():
	logout = False
	if 'username' not in login_session:
		logout = True
	genres = session.query(Genre).order_by(asc(Genre.name))
	return render_template('home.html',genres=genres,logout=logout)



@app.route('/home/newGenre/', methods=['POST','GET'])
# ''' Render page to add new genre
#     args : none

#     returns
#     newGenre template
#     logout : if user session exists
# ''' 
def newGenre():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = getUserID(login_session['email'])
        newGenre = Genre(name = request.form['genreName'],user_id=user_id)
        session.add(newGenre)
        session.commit()
        return redirect(url_for('home'))
    else:
		return render_template('newGenre.html',logout=False)

@app.route('/home/<int:genre_id>/',methods=['POST','GET'])
# ''' Render genre page with list of items  
#     args : 
#     genre_id : id of the genre

#     returns
#     genrePage template
#     logout : if user session exists(boolean)
#     genre : genre name
#     items : cursor containing items under this genre_id
#     user_id : email id of the user
#     editDelete : permission to edit or delete (boolean) 
# ''' 
def genrePage(genre_id):
    logout = True
    user_id = None
    editDelete = False
    if 'username' in login_session:
        logout = False
        user_id = getUserID(login_session['email'])
    
    genre = session.query(Genre).filter_by(id = genre_id).one()
    items = session.query(Albums).filter_by(genre_id = genre_id)
    if user_id == genre.user_id:
        editDelete = True
    return render_template('genrePage.html',genre=genre,
                            items=items,logout=logout,
                            user_id=user_id,editDelete=editDelete)



@app.route('/home/<int:genre_id>/delete/' , methods=['POST','GET'])
# ''' Render deleteGenre page 
#     function : delete genre and all its items  
    
#     args : 
#     genre_id : id of the genre

#     returns
#     home/deleteGenre template
#     logout : if user session exists(boolean)
# ''' 
def deleteGenre(genre_id):
	if 'username' not in login_session:
		return redirect(url_for('login'))
	genre = session.query(Genre).filter_by(id = genre_id).one()
	if (request.method == 'POST'):
	    session.delete(genre)
	    try:
                item = session.query(Albums).filter_by(id=genre_id).all()
                session.delete(item)
	    except:
                pass
            session.commit()
            flash('Successfully deleted genre')
            return redirect(url_for('home'))
        else:
            return render_template('deleteGenre.html',genre=genre,logout=False)




@app.route('/home/<int:genre_id>/edit/' , methods=['POST','GET'])
# ''' Render editGenre page 
#     function : update genre name  
    
#     args : 
#     genre_id : id of the genre

#     returns
#     home/editGenre template
#     logout : if user session exists(boolean)
#     genre : genre name
# ''' 
def editGenre(genre_id):
	if 'username' not in login_session:
		return redirect(url_for('login'))
	genre = session.query(Genre).filter_by(id = genre_id).one()
	if request.method == 'POST':
		genre.name = request.form['genreName']
		return redirect(url_for('home'))
	else:
		return render_template('editGenre.html',genre=genre,logout=False)



@app.route('/home/<int:genre_id>/<int:item_id>/edit', methods = ['POST','GET'])
# ''' Render editItem page 
#     function : update item information  
    
#     args : 
#     genre_id : id of the genre
#     item_id : id of the item to be updated

#     returns
#     home/editItem template
#     logout : if user session exists(boolean)
#     genre : cursor of the item
# ''' 
def editItem(genre_id,item_id):
	if 'username' not in login_session:
		return redirect(url_for('login'))
	item = session.query(Albums).filter_by(id=item_id).one()
	if request.method == 'POST':
	   if request.files['file']:
	       file = request.files['file']
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
	   if request.form['img_name']:
            item.img_name = request.form['img_name']
	   if request.form['name']:
	   	   item.name = request.form['name']
	   if request.form['disc']:
	   	   item.description = request.form['disc']
	   if request.form['price']:
	   	   item.price = request.form['price']
	   if request.form['type']:
	   	   item.p_type = request.form['type']
           session.add(item)
           session.commit()
	   return redirect(url_for('home'))
	else:
		
		return render_template('editItem.html',item=item,logout=False)



@app.route('/home/<int:genre_id>/addItem/' , methods=['POST','GET'])
# ''' Render additem page 
#     function : create new item  
    
#     args : 
#     genre_id : id of the genre

#     returns
#     home/addItem template
#     logout : if user session exists(boolean)
# ''' 

def addItem(genre_id):
   if 'username' not in login_session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      except:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'noimage.jpg'))
      name = request.form['name']
      disc = request.form['disc']
      price = request.form['price']
      p_type = request.form['type']
      try:
          img_name = request.form['img_name']
      except:
          img_name = 'noimage.jpg'
      user_id = getUserID(login_session['email'])
      # create new item
      newItem = Albums(name = name,description= disc,price=price,p_type=p_type,img_name=img_name,genre_id=genre_id,user_id=user_id)
      session.add(newItem)
      session.commit()
      flash('New item '+name+' added')
      return redirect(url_for('home'))
   else:
		return render_template('addItem.html',logout=False)


@app.route('/home/<int:genre_id>/addItem/<int:item_id>/',methods=["GET","POST"])
# ''' Render deleteItem page 
#     function : Delete an item  
    
#     args : 
#     genre_id : id of the genre
#     item_id : id of the item

#     returns
#     home/deleteItem template
#     logout : if user session exists(boolean)
#     item : name of the item that is deleated
# ''' 
def deleteItem(genre_id,item_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    item = session.query(Albums).filter_by(id = item_id).one()
    if request.method == "POST":
        os.remove( os.path.join(app.config['UPLOAD_FOLDER'],item.img_name) )
        session.delete(item)
        session.commit()
        flash('Item '+item.name+' deleted')
        return redirect(url_for('home'))
    else:
        return render_template('deleteItem.html',item=item,logout=False)


@app.route('/login/',methods=['GET','POST'])
# ''' Render login page 
#     function : create unique id for session and provide login functionalities  
    
#     args : None

#     returns
#     home/login template
#     logout : if user session exists(boolean)
#     state : unique string 
# ''' 
def login():
    logout = True
    if 'username' in login_session.keys():
        logout = False
    STATE = str( uuid.uuid4().hex )
    login_session['state'] = STATE
    return render_template('login.html',STATE=STATE,logout=logout)


@app.route('/home/JSON')
# ''' Render json data for the genre page 
#     args : None

#     returns
#     Json data
# ''' 
def genreJSON():
    genre = session.query(Genre).all()
    return jsonify(genre= [r.serialize for r in genre])


@app.route('/home/<int:genre_id>/JSON')
# ''' Render json data for the items page 
#     args : genre id

#     returns
#     Json data
# '''
def itemJSON(genre_id):
	item = session.query(Albums).filter_by(genre_id=genre_id).all()
	return jsonify(albums = [r.serialize for r in item])



@app.route('/home/XML')
# ''' Render XML data for the genre page 
#     args : None

#     returns
#     Json data
# '''
def genreXml():
    genre = session.query(Genre).all()
    return  Response(dicttoxml.dicttoxml( [r.serialize for r in genre] ), mimetype='text/xml')  


@app.route('/home/<int:genre_id>/XML')
# ''' Render json data for the genre page 
#     args : genre_id

#     returns
#     Json data
# '''
def itemXml(genre_id):
    item = session.query(Albums).filter_by(genre_id=genre_id).all()
    return Response( dicttoxml.dicttoxml ( [r.serialize for r in item] ),mimetype='text/xml' )


@app.route('/gconnect', methods=['POST'])
# ''' login using gmail 
    
#     returns:
#     user credentilas (name,email,image link)
# '''
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['provider'] = 'google'
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # check if user already exists
    if getUserID(data['email']) == None:
        createUser(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#Google DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    print 'In gdisconnect access token is %s', login_session
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        disconnect() 
    	# del login_session['gplus_id']
    	# del login_session['username']
    	# del login_session['email']
    	# del login_session['picture']
     #    del login_session['access_token']
     #    del login_session['state']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
        login_session.clear()
    	return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


#----------- Facebook Login --------------#

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secret.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secret.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# facebook DISCONNECT - Revoke a current user's token and reset their login_session 
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# ----------/ Facebook login--------------#





# ------------ User Helper Functions -----------------#

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['user_id']
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
    return 'Successfully logged out'



def createUser(login_session):
# '''
#     function : create user
#     args : login_session 

#     returns :
#     user_id : unique id of the created user 
# '''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# gets user info based on email id
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# get user id based on email id
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# run flask on port 8000
if __name__== "__main__":
 	app.secret_key = 'secret_key'
  	app.debug = True
  	app.run(host = '0.0.0.0', port = 8000)
