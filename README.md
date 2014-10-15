
# The Djangae Scaffold Project

This is a barebones Django project configured for use on App Engine using [https://github.com/potatolondon/djangae](Djangae)

To get started:

 - Clone this repo (don't forgot to change the origin to your own repo!)
 - Run ./install_deps (this will pip install requirements, and download the App Engine SDK)
 - python manage.py runserver

The install_deps helper script will install dependencies into a 'sitepackages' folder which is added to the path. Each time you run it your
sitepackages will be wiped out and reinstalled with pip. The SDK will only be downloaded the first time (as it's a large download).