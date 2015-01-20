# TalkDesk Integrator UI

This is a UI built to achieve

* Easier configuration of a talkdesk integration
* Hosted support for the webhooks required by integrations


### Running Locally

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

The app is already heroku ready. All you need to do is make sure you are on master and follow the commands below

```
heroku create
git push heroku master
```
The app is live on [https://talkdesk-integrator.herokuapp.com][1] 

[1]:https://talkdesk-integrator.herokuapp.com

### Progress

Here is the set of sub tasks this project has been divided into. Progress is being tracked here
- [x] UI to add Integration Configuration
- [ ] Link to the Json need to be given to TalkDesk for adding Integration
- [ ] UI to add Actions
