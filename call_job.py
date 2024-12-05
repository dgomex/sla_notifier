from os import environ

import jenkins

jenkins_server = jenkins.Jenkins(url=environ.get("JENKINS_HOST"),
                                 username=environ.get("JENKINS_USERNAME"),
                                 password=environ.get("JENKINS_PASSWORD"))

jenkins_server.build_job(name="remote_test")
