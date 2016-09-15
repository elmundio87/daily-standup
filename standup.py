import requests
import lxml.html
import config
import json
from jira import JIRA

def getRapidBoardId(board_name):
	url = "{0}/rest/greenhopper/1.0/rapidview".format(config.base_url)
	r = requests.get(url, auth=(config.user, config.password))
	boards = json.loads(r.text)
	for board in boards['views']:
		if board['name'] == board_name:
			return board['id']
	raise "No matching board found"

def getLatestSprint(id):
	url = "{0}/rest/greenhopper/latest/sprintquery/{1}".format(config.base_url, id)
	r = requests.get(url, auth=(config.user, config.password))
	sprints = json.loads(r.text)
	for sprint in sprints['sprints']:
		if sprint['state'] == "ACTIVE" and config.board in sprint['name']:
			return sprint['name']
	raise "No matching sprint found"

def getSprintGoals(sprint_name):
	url = "{0}/wiki/display/DEVOPSGUYS/{1}+Retrospective".format(config.base_url, sprint_name.replace(" ","+").replace("#",""))
	r = requests.get(url, auth=(config.user, config.password))
	r.raise_for_status

	rootElement = None

	tree = lxml.html.fromstring(r.text)

	elements = tree.find_class("innerCell")

	for element in elements:
		if "SprintGoals" in lxml.html.tostring(element):
			rootElement = element

	goals = rootElement.find('ul')
	return lxml.html.tostring(goals)

def getBlockedIssues(sprint_name):
	issues = "<ul>"
	jira = JIRA(config.base_url, basic_auth=(config.user, config.password))
	blocked = all_proj_issues_but_mine = jira.search_issues('Flagged = Impediment AND Sprint = "{0}"'.format(sprint_name))
	for issue in blocked:
		issues += "<li>"
		issues += "<a href=\"{0}\">".format(issue.key)
		issues += issue.key
		issues += "</a>"
		issues += issue.fields.summary
		issues += "</li>"
	issues += "</ul>"
	return issues

board_id = getRapidBoardId(config.board)
sprint_name = getLatestSprint(board_id)
print getBlockedIssues(sprint_name)
print getSprintGoals(sprint_name)
