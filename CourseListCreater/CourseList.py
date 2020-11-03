###############################################################
# Author: Yufeng Xing
# Date: 2020-11-03
###############################################################

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

reqs = requests.get('http://omscs.gatech.edu/current-courses')
reqs.encoding = 'utf-8'
soup = BeautifulSoup(reqs.text, 'html.parser')

Courses = []
htmls = []

# according to the webpages, all the courses are displayed in the <li> tag
for item in soup.find_all('li'):
    Courses.append(item.text.replace(u'\xa0', ' '))

# find all the texts related to the course
r = re.compile("\*?.*[0-9]{4}: .*")
Courses = list(filter(r.match, Courses))

# get the core type by '*', split the course id and course name
Courses = [['Core', i.split(':')[0][1:], i.split(':')[1]] 
           if i[0] == '*' 
           else 
           ['', i.split(':')[0], i.split(':')[1]] 
           for i in Courses]

# get all the links to the courses
for item in soup.find_all('li'):
    if r.match(item.text):
        if item.a:
            htmls.append(item.a.get('href'))
        else:
            htmls.append(None)

# add links to the given table
for index, item in enumerate(Courses):
    item.append(htmls[index])

# Split to get the appendix note of the courses
for item in Courses:
    if '(' in item[2]:
        item.append(item[2].split('(')[1][:-1])
        item[2] = item[2].split('(')[0]
        
# generate a data frame and save the information to csv
coursedf = pd.DataFrame(Courses, columns=['Type', 'CourseId', 'Name', 'Link', 'Note'])
coursedf.to_csv('OMSCSCourseList.csv')
