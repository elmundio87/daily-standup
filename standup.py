import requests
import lxml.html
import config

url = "https://devopsguys.atlassian.net/wiki/display/DEVOPSGUYS/Pack+2+Sprint+{0}+Retrospective".format(config.sprint)

r = requests.get(url, auth=(config.user, config.password))
r.raise_for_status

rootElement = None

tree = lxml.html.fromstring(r.text)

elements = tree.find_class("innerCell")

for element in elements:
	if "SprintGoals" in lxml.html.tostring(element):
		rootElement = element

goals = rootElement.find('ul').findall('li')

for goal in goals:
	print(lxml.html.tostring(goal))
