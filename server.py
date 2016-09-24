from flask import Flask, request
from flask_s3 import FlaskS3
from jira import JIRA
import config
import requests
import json
import lxml.html

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world", 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route("/getBlockedIssues")
def getBlockedIssues():
    
    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getBlockedIssues requires parameter [sprint_name]'
    
    jira = JIRA(config.base_url, basic_auth=(config.user, config.password))
    flagged  = jira.search_issues('Status NOT IN (Closed, Resolved) AND Flagged = Impediment AND Sprint = "{0}"'.format(sprint_name))
    with_customer = jira.search_issues('Status NOT IN (Closed, Resolved) AND Status = "With Customer" AND Sprint = "{0}"'.format(sprint_name))
    
    issues = []

    for issue in flagged:
        issues.append({"key":issue.key, "status":issue.fields.status.name, "description":issue.fields.summary, "flagged": True})
        
    for issue in with_customer:
        issues.append({"key":issue.key, "status":issue.fields.status.name, "description":issue.fields.summary, "flagged": False})


    if len(issues) == 0:
        return json.dumps({"error": "No blocked issues found."})
        
    return json.dumps({"issues":issues,"base_url":config.base_url})
    
@app.route("/getSprintGoals")
def getSprintGoals():
	
    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getBlockedIssues requires parameter [sprint_name]'

    url = "{0}/wiki/display/DEVOPSGUYS/{1}+Retrospective".format(config.base_url, sprint_name.replace(" ","+").replace("#",""))
    r = requests.get(url, auth=(config.user, config.password))
    r.raise_for_status

    tree = lxml.html.fromstring(r.text)

    elements = tree.find_class("innerCell")

    goals = None

    for element in elements:
        if ">Sprint Goals<" in lxml.html.tostring(element):
        	goals = element.find('ul')

    if goals == None:
        return "No Sprint goals found in {0}. Please ensure that {0} exists, and that there is a section called 'Sprint Goals' that contains a list.".format(url)

    return lxml.html.tostring(goals)

@app.route("/getRapidBoardId")
def getRapidBoardId():
    
    if 'board_name' in request.args:
        board_name = request.args['board_name']
    else:
        return 'getRapidBoardId requires parameter [board_name]'
    
    url = "{0}/rest/greenhopper/1.0/rapidview".format(config.base_url)
    r = requests.get(url, auth=(config.user, config.password))
    boards = json.loads(r.text)
    for board in boards['views']:
        if board['name'] == board_name:
            return json.dumps({"board_id": board['id']})
    return "No matching board found"

@app.route("/getSprintName")
def getSprintName():
    
    if 'board_id' in request.args:
        board_id = request.args['board_id']
    else:
        return 'getRapidBoardId requires parameter [board_id]'
    
    if 'board_name' in request.args:
        board_name = request.args['board_name']
    else:
        return 'getRapidBoardId requires parameter [board_name]'
        
    url = "{0}/rest/greenhopper/latest/sprintquery/{1}".format(config.base_url, board_id)
    r = requests.get(url, auth=(config.user, config.password))
    sprints = json.loads(r.text)
    for sprint in sprints['sprints']:
        if sprint['state'] == "ACTIVE" and board_name in sprint['name']:
            return json.dumps({"sprint_name": sprint['name']})
	
    return "No matching sprint found"
    
if __name__ == "__main__":
    app.run()
    
    
