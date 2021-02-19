# GrandPy_Bot
Single page web application built with Flask. 
A Grandpy Bot who can find the address of a place and tell us an anecdote about it. 
This app use MediaWiki and Google Maps APIs.

The backend is written in Python 
All scripts have been checked with pylint for PEP8 compliance
The webpage use Boostrap for responsiveness
The index.html script has been validated by W3C


# Files and folders

___gpb_app folder___
- api_manager.py : main script which parse the user input, get APIs data
- constants.py : stock variables for api_manager
- views.py : script for Flask app script
- static folder
    - style.scss is the css script for the web page
- images folder
- js folder
    - script.js is the script for front. Use to display the chat between the user and the bot and 
    to display Google Maps API. JQuery is used to display the bot answers without refresh the page.
- templates folder
    - index.html HTML script for the web page

__tests folder__
- test_api_manager.py : Unittest script for test the main script, api_manager

____
- requirements.txt contains all the required libraries for this program.
- run.py in the script to run for launching the GrandPy-Bot application

# Link

Link to the app, hosted by Heroku: https://jeanm-grandpy-bot.herokuapp.com/

# Install locally
- Clone the repo.
  ...
- Install and activate the virtual environment
  ...
- Install the required modules listed in requirements.txt
- indicate your personal Google Maps API key in gpb_app/api_manager.py at line 20
- Run the app with command : python run.py
- copy and paste the http://127.0.0.1:5000/ address in your browser

# GOOD TO KNOW
GrandPy only speak French...
be careful to indicate one place to search in your request to Grandpy...
- "connais tu openclassrooms ?" OK
- "connais tu openclassrooms à paris ?" NOT OK, will return paris infos

