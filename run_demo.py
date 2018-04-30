from __future__ import print_function
import os
import sys
import argparse
import json
import jenkins

CONFIG = {}
DEFAULT_FILE = 'defaults.json'
DUMMY_FLAG = 'dummy'
DUMMY_JOBS_FILE = 'dummy_jobs.json'


def initialize_parameters(input_args, defaults):
    """This is used to initialize the CONFIG dict.
    If the parametr is provided within the commandline arguments it's used,
    if not the default value read from the json 'defaults.json' file will be used

    Args:
        input_args (dict): The arguments provided through the cmd args.
        defaults (dict): The arguments read from the json defaults file.

    Returns:
        None

    """
    for param in defaults:
        CONFIG[param] = input_args.get(param) or defaults.get(param)
    return


def create_dummy_jobs(server):
    """This is used to initialize dummy jobs on jenkins server
    Only called if the '-d' or '--dummy' flag has been used while calling the script,
    If jobs with the same name already exist, they will be ignored and created again

    Args:
        server (jenkins.Jenkins): A connected jenkins server object.

    Returns:
        None

    """
    with open(DUMMY_JOBS_FILE, 'r') as f:
        dummy_jobs = json.load(f)

    for job in dummy_jobs:
        job_name = job.get('name')
        if not server.get_job_name(job_name):
            server.create_job(job_name, job.get('config'))
        if job.get('build'):
            server.build_job(job_name)
    return


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-ha', '--httpAddress', metavar='http_address',
                        help='Http address of the jenkins server')
    parser.add_argument('-hp', '--httpPort', metavar='http_address',
                        help='Http port of the jenkins server')
    parser.add_argument('-u', '--username', metavar='username',
                        help='Username to authenticate with jenkins server')
    parser.add_argument('-ps', '--password', metavar='password',
                        help='Password to authenticate with jenkins server')
    parser.add_argument('-d', '--dummy', action='store_true', dest=DUMMY_FLAG,
                        help='Use this flag if you want dummy jobs to be created automatically')

    # Parse the command line arguments, load the defaults and initialize the CONFIG parametrs
    args = parser.parse_args(arguments)
    with open(DEFAULT_FILE, 'r') as f:
        json_defaults = json.load(f)
    initialize_parameters(args.__dict__, json_defaults)

    # Connect to jenkins server and assure connection is succesful
    server = jenkins.Jenkins('http://{}:{}'.format(CONFIG['httpAddress'], CONFIG['httpPort']),
                             CONFIG['username'], CONFIG['password'])
    try:
        server.get_info()
    except jenkins.JenkinsException as jenkins_error:
        print("Jenkins error while connecting to server({}): {}".format(
            type(jenkins_error), jenkins_error))
        return

    # Create dummy jobs if specified by the dummy flag
    if CONFIG[DUMMY_FLAG]:
        create_dummy_jobs(server)
    # Get the jobs from the server, their names and their status
    jobs = server.get_jobs()
    ##############


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
