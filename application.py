from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
app.secret_key = "super secret key"

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Category, Item, Base

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Checks the login session to see if username exists, and if so assigns it.
# This will be used to display a logged in user.
def getUserName():
	if 'username' in login_session:
		return login_session['username']
	else:
		return ''

# Displays the catalog.
# Queries the database for all of the categories and the newest 5 itmes.
# Renders the html template for the catalog.
@app.route('/')
@app.route('/catalog')
@app.route('/catalog/')
def showCatalog():
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	categories = session.query(Category).order_by(asc(Category.name))
	items = session.query(Item).order_by(desc(Item.id)).limit(5)
	currentUser = getUserName()
	#currentUser = ''
	#if 'username' in login_session:
	#	currentUser = login_session['username']
	return render_template('catalog.html', categories = categories, items = items, currentUser = currentUser)


# Displays a specific category.
# Queries the database for all of the categories and off the items in that category.
# Renders the html template for the category.
@app.route('/catalog/category/<category_name>/')
@app.route('/catalog/category/<category_name>/items')
def showCategory(category_name):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	categories = session.query(Category).order_by(asc(Category.name))
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_ID = category.id)
	currentUser = getUserName()
	return render_template('categoryItems.html', categories = categories, category = category, items = items, currentUser = currentUser)

# Displays the item page.
# Queries the database for the current item and its category.
# Checks the email of the logged in user matches the creator of the item.
#if so, it renders the creator's html page which allows edit and delete. If
#it does not match, it will render the public item page.
@app.route('/catalog/category/<category_name>/items/<item_name>')
def showItem(category_name, item_name):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()
	currentUser = getUserName()
	if 'email' not in login_session or item.created_by != login_session['email']:
		return render_template('item.html', category = category, item = item, currentUser = currentUser)
	else: return render_template('itemCreator.html', category = category, item = item, currentUser = currentUser)


# Displays the create item form.
# Queries the database for the category of the item.
# If user is not logged in, redirects to login page.
# For GET: Renders the html template for the addItem html.
# For POST: submits form with: Item Name and Description provided by the user.
# The created_by field is taken from the login session, and the category from the current category. 
# By assigning the created_by field to the item, we forego the need to create a user data table.
@app.route('/catalog/category/<category_name>/items/new', methods=['GET', 'POST'])
def addItem(category_name):
	if 'username' not in login_session:
		return redirect('/login')
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	category = session.query(Category).filter_by(name = category_name).one()
	currentUser = getUserName()
	if request.method == 'POST':
		newItem = Item(name = request.form['name'], description = request.form['description'], created_by = login_session['email'], category_ID = category.id)
		session.add(newItem)
		session.commit()
		flash("New Item Created!")
		return	redirect(url_for('showCategory', category_name = category.name, currentUser = currentUser))
	else:
		return render_template('addItem.html', category_name = category.name, category = category, currentUser = currentUser)
	return "Created New Item"
	

# Displays the edit item page.
# Queries the database for the current category and item.
# Checks if current user is the creator of the item(preventing direct URL access as well). If
#user is not the creator, gives an error or redirects to login.
# POST: Updates the item name or description.
# GET: Renders the html template for the edit form.
@app.route('/catalog/category/<category_name>/items/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	if 'username' not in login_session:
		return redirect('/login')
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()
	currentUser = getUserName()
	if item.created_by != login_session['email']:
		return "<script>function myFunction() {alert('You are not authorized to edit this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		session.add(item)
		session.commit()
		flash('Item Edited.')
		return redirect(url_for('showCategory', category_name = category.name, currentUser = currentUser))
	else:
		return render_template('editItem.html', category_id = category.id, item_name = item.name, category = category, item = item, currentUser = currentUser)

# Displays the delete item page.
# Queries the database for the current category and item.
# Checks if current user is the creator of the item(preventing direct URL access as well). If
#user is not the creator, gives an error or redirects to login.
# POST: Deletes the item.
# GET: Renders the html template for the delte form.
@app.route('/catalog/category/<category_name>/items/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
	if 'username' not in login_session:
		return redirect('/login')
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()
	currentUser = getUserName()
	if item.created_by != login_session['email']:
		return "<script>function myFunction() {alert('You are not authorized to delete this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('Item Deleted')
		return redirect(url_for('showCategory', category_name = category.name, currentUser = currentUser))
	else:
		return render_template('deleteItem.html', category_name = category.name, item_name = item.name, category = category, item = item, currentUser = currentUser)


# Displays the login page.
# The only current option is a google Oauth. A google account is required to log in.
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE = state)

# Provided by the google documentation and classroom code. 
@app.route('/gconnect', methods=['POST'])
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
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
        return response

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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

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

# Logout from Google Oauth and delete the login session.
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return response

# API endpoint for JSON output for an item.
@app.route('/json/<category_name>/items/<item_name>')
def showItemJSON(category_name, item_name):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	category = session.query(Category).filter_by(name = category_name).one()
	item = session.query(Item).filter_by(name = item_name).one()

	return jsonify(item= item.serialize)
	#jsonify(item = item.serialize)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)