# _URL Shortner_
## Introduction
The URL Shortener app is a web application built using Django that allows users to shorten long URLs into compact, shareable links. By using this app, users can transform lengthy web addresses into shorter versions that are easier to remember, share, and distribute across different platforms.

In addition to shortening URLs, the app also provides valuable insights by tracking key usage statistics such as the number of times a shortened link is clicked etc.

## Main features

* Simple and Easy set-up
* Create and manage short urls
* Url usage statistics

## Usage

To use this project follow the below instructions:

## Getting Started

First clone the repository from GitHub:

    $ git clone https://github.com/yk2408/url-shortener.git
    

Create a Python Virtual environment:

    $ python -m venv myvenv
    
Activate the virtualenv for your project.
     
    Windows
        $ myvenv/Scripts/activate
    
    Linux :
        $ source myvenv/bin/activate
     
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver