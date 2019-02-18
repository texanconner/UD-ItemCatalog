# UD-ItemCatalog
Project Description:
This web application is a simple catalog of items organized by categories.

# Functionality:
Guest users can view the catalog page, a specific category, a specific item, or even create a new item.
Editing or deleting an item requires a user to log in, and only the creator of that item can do so.
Login can only be done with Google Oath, so a google account is required.
JSON endpoint API's return serailzed JSON dat for a specified item.

# Requirements
I used the VM and Vagrant setup from the class documents.
https://www.udacity.com/wiki/ud088/vagrant

From there I cloned the Full Stack VM repository.
http://github.com/udacity/fullstack-nanodegree-vm&sa=D&ust=1547093291759000

These files can be put there into that catalog folder in the Full Stack VM Repo.

A client_secrets.JSON file will also be needed, which can be retrieved from the Google Oauth page. This will be placed in the catalog folder.

Python 3.7.1 was used to test this app

SQL Alchemy is used for the database management.
`pip install SQLAlchemy`

Flask is used for the web management.
`pip install Flask`

# Database Setup
In the vagrant session, inside the catalog folder, run the catalog_db_setup.py file.
This will create the database needed.

Next add the default items and categories by running the add_catalog_items.py file.


# Application
From the vagrant session, in the catalog folder, run the application.py file.

From your web browser go to http://localhost:5000/catalog/ 

The application should be up and working there. 

To retrieve JSON data you will need to know your category and item request. The format to request the URL is: http://localhost:5000/json/<category_name>/items/<item_name>

Example: http://localhost:5000/json/Basketball/items/Hoop

# HTML and CSS
Flask Templates were used for the HTML and can be found in the catalog/templates folder

I initially made my own CSS(in the static folder), but them added bootstrap CDN to handle the CSS and layout. The current CSS folder is blank, but I may customize more at a late point.
