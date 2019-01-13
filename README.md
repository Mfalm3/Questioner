# Questioner API v1.

[![Build Status](https://travis-ci.org/Mfalm3/Questioner.svg?branch=develop)](https://travis-ci.org/Mfalm3/Questioner)
[![Maintainability](https://api.codeclimate.com/v1/badges/d1288bf7e1e753038ced/maintainability)](https://codeclimate.com/github/Mfalm3/Questioner/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4c78f944adca45ce969d5abc44429d6b)](https://www.codacy.com/app/Mfalm3/Questioner?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Mfalm3/Questioner&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/Mfalm3/Questioner/badge.svg?branch=develop)](https://coveralls.io/github/Mfalm3/Questioner?branch=develop)

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log

## Basic Features

### An API with endpoints where
1. Admins can create a meetup.
2. Users can create a question in a meetup.
3. Users can get a specific meetup record.
4. Users can get all meetup records.
5. Users can upvote or downvote a question.
6. Users can RSVP for a meetup.

## Requirements
1. git
2. python3
3. pip
4. postman

## Getting Started
#### 1. Clone the repository
`$ git clone https://github.com/Mfalm3/Questioner.git`

#### 2. Checkout to the develop branch
`$ git checkout develop`

#### 3. Ensure you have python 3 on your device
`$ python3 --version`
if not installed view installation details from [official website](https://www.python.org/)

#### 4. Ensure you have pip installed
`$ pip --version`
if not installed, view installation details from [pip website](https://pip.pypa.io/en/stable/installing/)

#### 5. Install virtualenv
`$ pip install virtualenv`

#### 6. CD into the cloned repository's directory
`$ cd /path/to/Questioner`
#### 7. Create and Activate virtual environment
`$ virtualenv venv`
`$ source venv/bin/activate`

#### 8. Install the required dependancies
`$ pip intall -r requirements.txt`

#### 9. Run the app
`$ python run.py`

#### 10. Use postman to test the following endpoints

| Endpoints                                  |               Functions                |
| ------------------------------------------ | :------------------------------------: |
| POST/api/v1/signup                         |            create new user             |
| POST/api/v1/login                          |        sign in to your account         |
| POST/api/v1/meetups                        |             create meetups             |
| GET/api/v1/meetups/&lt;id&gt;              |         get a specific meetups         |
| GET/api/v1/meetups/upcoming                |        get all upcoming meetups        |
| POST/api/v1/questions                      |       add question to a meetup         |
| POST/api/v1/meetups/&lt;id&gt;/rsvp        |     respond to meetups invitation      |
| PATCH/api/v1/questions/&lt;id&gt;/upvote   |           upvote a question            |
| PATCH/api/v1/questions/&lt;id&gt;/downvote |          downvote a question           |
| POST/api/v1/questions/&lt;id&gt;/          |        view a specific question        |

#### Testing
`$ pytest`

### Heroku
This API is hosted on Heroku at https://qmeetups.herokuapp.com. There is no default route that has been configured but you can test the API's endpoints by providing their paths after the host name. For instance, to test user account registration navigate to https://qmeetups.herokuapp.com/signup.

#### Acknowledgements
1. Andela workshops
2. Team mates

#### Author
Joe Waithaka
