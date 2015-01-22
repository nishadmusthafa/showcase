# TalkDesk Integrator UI

This is a UI built to achieve

* Easier configuration of a talkdesk integration
* This can be thought of as a reusable "bridge" as described [here][1]

[1]:https://github.com/Talkdesk/api/tree/master/integrations

### Running Locally

Please add an environment variable DEBUG and set its value to "True". Then use the following commands. 

```
git clone https://github.com/iHacketh/tech_challenge.git
workon integrator_env
pip install -r requirements.txt
python manage.py runserver
```
You will need python virtual environment helpers for "workon" to work

### Running Tests

```
pip install -r test_requirements.txt
python manage.py test functional_tests
```

### Deployment

The app is already heroku ready.  You will need to add two Config Vars to your heroku app  
```
MONGO_DB_NAME - Your mongo db name
MONGO_URI - mongodb://{user}:{pwd}@{host}:{port}/MONGO_DB_NAME
```
Make sure you are on master branch and execute the following commands.

```
heroku create
git push heroku master
```
The app is live on [https://talkdesk-integrator.herokuapp.com][2] 

[2]:https://talkdesk-integrator.herokuapp.com

### Progress

Here is the set of sub tasks this project has been divided into. Progress is being tracked here
- [x] UI to add Integration Configuration
- [ ] Link to the Json need to be given to TalkDesk for adding Integration
- [ ] UI to add Actions
