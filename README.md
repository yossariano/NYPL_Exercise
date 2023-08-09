# NYPL Exercise
Coding exercise using NYPL Digital Collections API.
Uses flask to run a simple Python webapp. See instructions below for environment setup.

# Setup
Set up a virtualenv when checking out this package.

```
pip3 install virtualenv
virtualenv env
source env/bin/activate

# You should now be in your virtual env

# Install flask in virtualenv
pip3 install flask
```

# Running the app
The following script will start up the virtualenv if not running and start your flask server:

```
./start-server.sh
```

# Leaving virtualenv
If you want to leave your virtualenv, simply run:

```
deactivate
```
