import requests
import lxml.html
import config
from jira import JIRA

def getSprintGoals():
	url = "https://devopsguys.atlassian.net/wiki/display/DEVOPSGUYS/Pack+2+Sprint+{0}+Retrospective".format(config.sprint)

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

def getBlockedIssues():
	issues = ""
	jira = JIRA('https://devopsguys.atlassian.net', basic_auth=(config.user, config.password))
	blocked = all_proj_issues_but_mine = jira.search_issues('Flagged = Impediment AND Sprint = "Pack 2 Sprint #{0}"'.format(config.sprint))
	for issue in blocked:
		issues += issue.key
		issues += " : "
		issues += issue.fields.summary
	print issues

getBlockedIssues()
getSprintGoals()
