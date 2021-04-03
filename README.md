# Social Media Backend With Django Framework

## About

This project is the backend server of a social media app with following features:
 - A user can sign up and login with unique e-mail and username
 - Users can update their full_name, bio and profile_photo
 - A user can follow and unfollow other users
 - They can see the people they follow, and the people who follow them
 - A user can post a photo
 - A user can see the posts of the people who they follow

## How to run
 - Download or clone the project
 - Run the command "python3 manage.py runserver" on the 'scorp_project' folder
 - You can go to http://localhost:8000/scorp/ addres from your browser or you can use Postman to send requests

## Pre-requests
 - Mysql server needs to be running on the localhost. You can change db settings from the
scorp_project/settings.py file.

## Endpoints
 - You can import the postman collection file under the /postman_requests and start experimenting on endpoints