#!/usr/bin/python
# -*- coding: utf8 -*-

import json
import urllib2
import os
from subprocess import call

LOCAL_FOLDER = '/srv/git/'
GITHUB_USERNAME = 'paalka'
GITHUB_API_URL = "https://api.github.com/"

def update_repo(path_to_repo, description):
    orig_directory = os.getcwd()
    os.chdir(path_to_repo)

    call(["git", "fetch", "--force"])
    call(['git', 'config', '--local', '--replace-all', 'gitweb.description', description])

    os.chdir(orig_directory)


def clone_repo(repo_url, repo_description, store_location):
    call(["git", "clone", "--mirror",
          "--config", "gitweb.description=" + repo_description,
          repo_url, store_location])


def update_repos(repos_to_update, repos_location):

    for repo in repos_to_update:
        path_to_repo = os.path.join(repos_location, repo["name"])

        if os.path.isdir(path_to_repo):
            update_repo(path_to_repo, repo["description"])
        else:
            clone_repo(repo["git_url"], repo["description"], path_to_repo)


def get_repos(username):
    # Since github limits the amount of repos received, set the max to
    # something large.
    url = GITHUB_API_URL + "users/" + username + "/repos?per_page=1000"
    response = urllib2.urlopen(url)
    repo_data = None

    if response:
        repo_data = json.loads(response.read())

    return repo_data


def main():
    repos = get_repos(GITHUB_USERNAME)
    update_repos(repos, LOCAL_FOLDER)


if __name__ == '__main__':
    main()
