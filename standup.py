import requests
import lxml.html
import config
import json
from jira import JIRA
import time
import webbrowser
import os

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

def getSprintGoals(sprint_name):
	print("Getting sprint goals")
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

def getBlockedIssues(sprint_name):
	print("Getting blocked issues")
	issues = "<ul class='no-bullet-points'>"
	jira = JIRA(config.base_url, basic_auth=(config.user, config.password))
	blocked = all_proj_issues_but_mine = jira.search_issues('Status NOT IN (Closed, Resolved) AND Flagged = Impediment AND Sprint = "{0}"'.format(sprint_name))

	if blocked == []:
		return "No Blocked issues found in {0}. Any issue that is flagged will be counted as 'Blocked'".format(sprint_name)

	for issue in blocked:
		issues += "<li>"
		issues += "<div class='card'>"
		issues += "<div style='float:left'>"
		issues += "<a target='_blank' href=\"{0}/browse/{1}\">".format(config.base_url, issue.key)
		issues += issue.key
		issues += "</a>"
		issues += "</div>"
		issues += "<div style='float:right;font-weight: bold''>"
		issues += issue.fields.status.name
		issues += "</div>"
		issues += "<div style='float:left'>"
		issues += issue.fields.summary.replace("Why:","</br>Why:")
		issues += "</div>"
		issues += "</div>"
		issues += "</li>"
	issues += "</ul>"
	return issues

def getTotalPoints(sprint_name):

	jira = JIRA(config.base_url, basic_auth=(config.user, config.password))
	closed_issues = all_proj_issues_but_mine = jira.search_issues('Status IN (Closed, Resolved) AND Sprint = "{0}"'.format(sprint_name))
	open_issues = all_proj_issues_but_mine = jira.search_issues('Status NOT IN (Closed, Resolved) AND Sprint = "{0}"'.format(sprint_name))

	total_points_open = 0
	total_points_closed = 0

	for issue in closed_issues:
		if config.story_points_custom_field in issue.fields.__dict__.keys():
			points = getattr(issue.fields, config.story_points_custom_field)
			if points != None:
				total_points_closed += points

	for issue in open_issues:
		if config.story_points_custom_field in issue.fields.__dict__.keys():
			points = getattr(issue.fields, config.story_points_custom_field)
			if points != None:
				total_points_open += points

	return (total_points_open, total_points_closed)

board_id = getRapidBoardId(config.board)
sprint_name = getLatestSprint(board_id)

with open('index.html.template', 'r') as html_file:
    data=html_file.read()

data = data.replace("@SPRINT_GOALS@",getSprintGoals(sprint_name))
data = data.replace("@BLOCKED_ISSUES@",getBlockedIssues(sprint_name))
data = data.replace("@DISPLAY_NAME@","{0} - {1}".format(sprint_name,time.strftime("%x")))

text_file = open("index.html", "w")
text_file.write(data)
text_file.close()

print("Created index.html")
dir_path = os.path.dirname(os.path.realpath(__file__))
webbrowser.open('file://{0}/index.html'.format(dir_path))
