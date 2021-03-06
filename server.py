from functools import wraps
from flask import Flask, request, Response
from jira import JIRA
import sys
import requests
import json
import lxml.html
import re
from Crypto.Hash import SHA256
from retrying import retry
from datetime import datetime, date, timedelta
from config import config
from lib import expiring_certs
from lib import working_days

app = Flask(__name__)


@retry(stop_max_attempt_number=10)
def request_page_with_authentication(url, username, password):
    r = requests.get(url, auth=(username, password))

    # Sometimes the Atlassian server rejects the password
    # so retry a few times
    if r.status_code == 401:
        raise Exception

    return r


def find_in_confluence_page(sprint_name, search_string, child_element, label):
    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getSprintActions requires parameter [sprint_name]'

    url = "{0}/wiki/display/DEVOPSGUYS/{1}+Retrospective".format(
        config.base_url, sprint_name.replace(" ", "+").replace("#", ""))

    r = request_page_with_authentication(url, config.atlassian_username,
                                         config.atlassian_password)
    r.raise_for_status

    tree = lxml.html.fromstring(r.text)

    elements = tree.find_class("innerCell")

    actions = None

    for element in elements:
        if search_string in lxml.html.tostring(element):
            actions = element.find(child_element)

    if actions is None:
        return "Nothing found in Confluence. Please ensure that <a href='{1}'>this page</a> exists, and that there is a section called '{1}'".format(url, label), 200

    return lxml.html.tostring(actions), 200


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    h = SHA256.new()
    h.update(password)
    auth_password_sha256 = h.hexdigest()
    return username == config.auth_username and auth_password_sha256 == config.auth_password_sha256


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def index():
    return "Hello world", 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.route("/getBlockedIssues")
@requires_auth
def getBlockedIssues():

    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getBlockedIssues requires parameter [sprint_name]', 400

    jira = JIRA(config.base_url, basic_auth=(
        config.atlassian_username, config.atlassian_password))
    flagged = jira.search_issues(
        'Status NOT IN (Closed, Resolved) AND Flagged '
        '= Impediment AND Sprint = "{0}"'.format(sprint_name))
    with_customer = jira.search_issues(
        'Status NOT IN (Closed, Resolved) AND Status = "With Customer" AND '
        'Sprint = "{0}"'.format(sprint_name))

    issues = []

    for issue in flagged:
        startDate = issue.fields.updated
        # comments = jira.comments(issue)
        # if len(comments) > 0:
        #     startDate = comments[-1].updated

        startDate = re.sub('\..*', '', startDate)
        startDate = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S').date()
        endDate = date.today()
        last_update_days = "{0}".format(working_days.get_working_days(startDate, endDate))
        if len(filter(lambda x: x['key'] == issue.key, issues)) == 0:
            issues.append({"key": issue.key,
                           "status": issue.fields.status.name,
                           "description": issue.fields.summary,
                           "flagged": True,
                           "last_update_days": last_update_days})

    for issue in with_customer:
        startDate = issue.fields.updated
        comments = jira.comments(issue)
        if len(comments) > 0:
            startDate = comments[-1].updated

        startDate = re.sub('\..*', '', startDate)
        startDate = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S').date()
        endDate = date.today()
        last_update_days = "{0}".format(working_days.get_working_days(startDate, endDate))
        if len(filter(lambda x: x['key'] == issue.key, issues)) == 0:
            issues.append({"key": issue.key,
                           "status": issue.fields.status.name,
                           "description": issue.fields.summary,
                           "flagged": False,
                           "last_update_days": last_update_days})

    if len(issues) == 0:
        return json.dumps({"error": "No blocked issues found. Any issue that "
                           "is flagged or 'With Customer' is counted as "
                           "'Blocked'"})

    return json.dumps({"issues": issues, "base_url": config.base_url}), 200


@app.route("/getSprintGoals")
@requires_auth
def getSprintGoals():

    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getSprintGoals requires parameter [sprint_name]'

    return find_in_confluence_page(sprint_name, '>Sprint Goals<', 'ul', 'Sprint Goals')


@app.route("/getSprintActions")
@requires_auth
def getSprintActions():

    if 'sprint_name' in request.args:
        sprint_name = request.args['sprint_name']
    else:
        return 'getSprintActions requires parameter [sprint_name]'

    return find_in_confluence_page(sprint_name, '>Actions<', 'ul', 'Actions')


@app.route("/getRapidBoardId")
@requires_auth
def getRapidBoardId():

    if 'board_name' in request.args:
        board_name = request.args['board_name']
    else:
        return 'getRapidBoardId requires parameter [board_name]'

    url = "{0}/rest/greenhopper/1.0/rapidview".format(config.base_url)
    r = request_page_with_authentication(url, config.atlassian_username,
                                         config.atlassian_password)
    boards = json.loads(r.text)
    for board in boards['views']:
        if board['name'] == board_name:
            return json.dumps({"board_id": board['id']}), 200
    return "No matching board found", 200


@app.route("/getSprintDaysRemaining")
@requires_auth
def getSprintDaysRemaining():

    if 'board_id' in request.args:
        board_id = request.args['board_id']
    else:
        return 'getSprintEndDate requires parameter [board_id]', 400

    if 'sprint_id' in request.args:
        sprint_id = request.args['sprint_id']
    else:
        return 'getSprintEndDate requires parameter [sprint_id]', 400

    url = "{0}/rest/greenhopper/1.0/rapid/charts/sprintreport/?rapidViewId={1}&sprintId={2}".format(
        config.base_url, board_id, sprint_id)
    r = request_page_with_authentication(url, config.atlassian_username,
                                         config.atlassian_password)
    sprint_report = json.loads(r.text)

    startDate = date.today()
    endDate = datetime.strptime(sprint_report["sprint"][
                                "endDate"], '%d/%b/%y %H:%M %p').date()

    return "{0}".format(working_days.get_working_days(startDate, endDate)), 200


@app.route("/getSprintName")
@requires_auth
def getSprintName():

    if 'board_id' in request.args:
        board_id = request.args['board_id']
    else:
        return 'getRapidBoardId requires parameter [board_id]', 400

    if 'board_name' in request.args:
        board_name = request.args['board_name']
    else:
        return 'getRapidBoardId requires parameter [board_name]', 400

    url = "{0}/rest/greenhopper/latest/sprintquery/{1}".format(
        config.base_url, board_id)
    r = request_page_with_authentication(url, config.atlassian_username,
                                         config.atlassian_password)
    sprints = json.loads(r.text)
    for sprint in sprints['sprints']:
        if sprint['state'] == "ACTIVE" and board_name in sprint['name']:
            return json.dumps({
                "sprint_name": sprint['name'],
                "sprint_id": sprint['id']}), 200

    return "No matching sprint found", 400


@app.route("/getExpiringCertificates")
def getExpiringCertificates():

    if 'board_name' in request.args:
        board_name = request.args['board_name']
    else:
        return 'getExpiringCertificates requires parameter [board_name]', 400

    return expiring_certs.get_expiring_certs(board_name), 200

if __name__ == "__main__":
    app.run(threaded=True)
