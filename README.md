# NYPL Exercise
Coding exercise using NYPL Digital Collections API.
Uses flask to run a simple Python webapp.

The purpose of this webapp is to show simple integration with the NYPL Digital Collections API-
it does so by taking a URL search parameter and displaying a random image from the digital catalogue
corresponding to the user's search. While intended to vend animal images at random, a user could feasibly
search for any randomized image they desire.

**Note**: Requires an auth token to access the NYPL API. See instructions below.

# Setup
Set up a virtualenv when checking out this package.

```
pip3 install virtualenv
virtualenv env
source env/bin/activate

# You should now be in your virtual env

# Install dependencies in virtualenv
pip3 install -r requirements.txt

# Write your NYPL digital collections access token to a file
AUTH_TOKEN='<insert your token here>'
echo "$AUTH_TOKEN" > nypl_token.txt
```

# Running the app
The following script will start up the virtualenv if not running and start your flask server:

```
./start-server.sh
```

Once running, you can access your server and make a request for a random animal image like so:

```
http://127.0.0.1:5000/randimal/pig
```

# Testing
Run unit tests with pytest from within your virtualenv:

```
./run-tests.sh
```

# Leaving virtualenv
If you want to leave your virtualenv, simply run:

```
deactivate
```
