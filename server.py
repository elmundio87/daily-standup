from flask import Flask
from jira import JIRA
import config
import requests
import json
import lxml.html

app = Flask(__name__, static_url_path='')

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/getBlockedIssues")
def getBlockedIssues():
	
    jira = JIRA(config.base_url, basic_auth=(config.user, config.password))
    flagged  = jira.search_issues('Status NOT IN (Closed, Resolved) AND Flagged = Impediment AND Sprint = "{0}"'.format(sprint_name))
    with_customer = jira.search_issues('Status NOT IN (Closed, Resolved) AND Status = "With Customer" AND Sprint = "{0}"'.format(sprint_name))
    
    issues = []

    for issue in flagged:
        issues.append({"key":issue.key, "status":issue.fields.status.name, "description":issue.fields.summary, "flagged": True})
        
    for issue in with_customer:
        issues.append({"key":issue.key, "status":issue.fields.status.name, "description":issue.fields.summary, "flagged": False})

    return json.dumps({"issues":issues,"base_url":config.base_url})
    
@app.route("/getSprintGoals")
def getSprintGoals():
	
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

def getRapidBoardId(board_name):
	url = "{0}/rest/greenhopper/1.0/rapidview".format(config.base_url)
	r = requests.get(url, auth=(config.user, config.password))
	boards = json.loads(r.text)
	for board in boards['views']:
		if board['name'] == board_name:
			print("Found board ID {0}".format(board['id']))
			return board['id']
	raise "No matching board found"

def getLatestSprint(id):
	url = "{0}/rest/greenhopper/latest/sprintquery/{1}".format(config.base_url, id)
	r = requests.get(url, auth=(config.user, config.password))
	sprints = json.loads(r.text)
	for sprint in sprints['sprints']:
		if sprint['state'] == "ACTIVE" and config.board in sprint['name']:
			print("Found sprint name {0}".format(sprint['name']))
			return sprint['name']
	raise "No matching sprint found"

if __name__ == "__main__":
    board_id = getRapidBoardId(config.board)
    sprint_name = getLatestSprint(board_id)
    app.run()
    
    
