from dotenv import load_dotenv
from pprint import pprint

import json
import requests
import time
import links_from_header
import os.path


load_dotenv()

## Env Example
# course_id = '2568966'  # P2
# quiz_id = '7102275'
# token='XPTO'

token = os.getenv("token")
header = {'Authorization': 'Bearer ' + '%s' % token}
course_id = os.getenv("course_id")
download_quiz_id = os.getenv("quiz_id")

def get_data(addr, paginate=True):
    url = 'https://canvas.instructure.com/api/v1/courses/' + course_id + '/' + addr
    r = requests.get(url, headers=header )
    if r.status_code == 404:
        raise Exception("404 Not Found")
    data = r.json()
    result = []
    if isinstance(data, (list, tuple)):
        result = list(data)
    else:
        result = [data]
    if not paginate:
        return result
    if 'Link' in r.headers:
        links = links_from_header.extract(r.headers['Link'])
        while 'next' in links:
            url = links['next']
            r = requests.get(url, headers=header )
            data = r.json()
            if isinstance(data, (list, tuple)):
                result.extend(data)
            else:
                result.append(data)
            links = links_from_header.extract(r.headers['Link'])
        
    return result


quiz_data = get_data('quizzes/')

answers = []

for quiz in quiz_data:
    quiz_id = str(quiz['id'])
    if quiz_id != download_quiz_id:
        continue
    title = quiz['title']
    due_at = quiz['due_at']
    assignment_id = str(quiz['assignment_id'])

    question_data = get_data('quizzes/' + quiz_id + '/questions') 
    questions = {}
    for question in question_data:
        question_id = question['id']
        question_text = question['question_text']
        questions[question_id] = question_text
    questions_fname = 'questions_' + quiz_id + '.json'
    open(questions_fname, 'w').write(json.dumps(question_data))
    sub_data = get_data('assignments/' + assignment_id + '/submissions?include[]=submission_history')
    open('sub_' + quiz_id + '.json', 'w').write(json.dumps(sub_data))
