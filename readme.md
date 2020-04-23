# This repo scraps the results of my classmates from the jntuh(university) website and upload it to mysql database.

## Requirements
- python
    - beautiful soup
    - mysql connector
    - requests
- mysql server
- apache webserver

## Running
- Run schema.sql to create sql database and table to store results.
- Run jntuh_results.py to scrape the data and upload it to sql table.
- Open display_results.php to display results in form of table.

## Some Background
- The results website had a text captcha before submiting the form to retrieve the result.
- Grabbing the image and use opencv to detect text from the image and post it to get the result was an option.
- But I found its not an image but its just text with disabled html attribute.
- I could just get the text from the tag and post it.
- But when I analysed the request I found no captcha text is being sent, only the rollno and other parameters are being sent.
- Even the session id is not being tested if it is valid or not.(Its dumb of them).
- So I wrote a python script to just post the rollno's(stored in an array).
- Then calculated the overall score based on subject wise points and stored in sql table.
- Then the results are displayed on my website using php script.
- The results displayed are sortable column-wise in the order O > A+ > A > B+ > B > C > F.

## Demo
https://andeyashwanth.tk/JNTUHResults/31_results.php
