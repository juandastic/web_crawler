# Custom Crowl
This is a fork of  [crowl](https://gitlab.com/crowltech/crowl) an open-source SEO crawler.
[Official docs](https://www.crowl.tech/docs/)


## Setup

This version use docker to create and Pyhton container and Mysql container to process and store all the collected data

You need at least 
- docker-compose version 1.23.2
- Docker version 18.09.2

## Build the image and run all container

You have to run
`` docker-compose up -d ``

That would start two containers one with the crawler script and another with the database the name of these containers should be something like:
```
web_crawler_db_1
web_crawler_app_1
```
Where ``web_crawler``is the name of the parent folder of the docker-compose.yml file

## Start a crawl

The app container initializes a Linux with python 3 installed but it doesn't run the crawler, to start we need to enter inside the container and run it manually

``docker exec -it web_crawler_app_1 /bin/bash ``

with that command we open a terminal inside the container, then we could start the crawler script

Single page crawl 
`` python crowl.py --conf la_haus_med_srp.ini ``

Whole website crawl *8h*
`` python crowl.py --conf la_haus_global.ini ``
