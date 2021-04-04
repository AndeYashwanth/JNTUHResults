# This repo scraps the results of my classmates from the jntuh(university) website and upload it to mysql database.

## Requirements
- python
    - beautiful soup
    - mysql connector python
    - requests
    - python dotenv
- mysql server
- apache webserver

## Running
- Create a database and add the details in `.env` file and `display_results.php` file

- paste the result URL of JNTU in `.env` file

- Add roll numbers in `rollnos` array in `jntuh_results.py` file

- Run jntuh_results.py to scrape the data and upload it to MySQL table.

- Open `https://domainname:port/display_results.php?examcode=<enter examcode here>` to display results in form of table.

  Note: examcode can be found in url.

## Some Background
- The results website had a text captcha before submiting the form to retrieve the result.
- Grabbing the image and use opencv to detect text from the image and post it to get the result was an option.
- But I found its not an image but its just text with disabled html attribute.
- I could just get the text from the tag and post it.
- But when I saw the request in network tab I found no captcha text is sent, only the rollno and other parameters are being sent.
- Even the session id/cookie is not being validated.(Its so dumb).
- So I wrote a python script to send post request for each of the rollno's(stored in an array).
- Then calculated the grade and stored in sql table.
- Then the results are displayed using `display_results.php` script.
- The results displayed are sortable column-wise in the order O > A+ > A > B+ > B > C > F.
