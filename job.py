import os
from os import environ

import datetime
import jenkins
import yaml


class Job:
    def __init__(self, name: str, sla_time: str,
                 jenkins_host=environ.get("JENKINS_HOST"),
                 jenkins_username=environ.get("JENKINS_USERNAME"),
                 jenkins_password=environ.get("JENKINS_PASSWORD"),
                 status: str = "Unknown"):
        self.name = name
        # SLA TIME = SLA TIME FROM FILE + SLA INCREASE FROM ENV VAR SLA_INCREASE
        self.sla_time = str(datetime.datetime.strptime(f"{datetime.date.today()} {sla_time}:00",
                                                       "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            minutes=int(os.getenv("SLA_INCREASE", 0))))
        self.server = jenkins.Jenkins(url=jenkins_host, username=jenkins_username, password=jenkins_password)
        self.status = status

    def __str__(self):
        return f"Job name={self.name}, status={self.status}, SLA={self.sla_time}"

    @classmethod
    def read_from_yaml(cls, file_path=environ.get("SLA_CONFIG_PATH")):
        jobs = []
        try:
            with open(file_path, "r") as file:
                print(f"Reading input for job objects from {file_path}")
                yaml_data = yaml.load(file, Loader=yaml.FullLoader)

            if yaml_data:
                for job_info in yaml_data:
                    job = job_info.get("Job")
                    if job:
                        table_config = cls(
                            name=job.get("name"),
                            sla_time=job.get("sla_time")
                        )
                        jobs.append(table_config)
            return jobs
        except Exception as e:
            print(f"An error occurred while reading the YAML file: {e}")
            raise Exception

    def get_job_last_build_info(self):
        try:
            print(self.server.get_job_info(self.name))
            last_build_number = self.server.get_job_info(self.name)["lastCompletedBuild"]["number"]
            build_info = self.server.get_build_info(self.name, last_build_number)
            started_epoch = build_info["timestamp"]
            started_timestamp = datetime.datetime.fromtimestamp(started_epoch / 1000).strftime("%Y-%m-%d %H:%M:%S")
            last_build_info = {"started_timestamp": started_timestamp, "build_status": build_info["result"]}
            print(f"{self.name} - SLA set: {self.sla_time}")
            print(f"{self.name} - Last build info: {last_build_info}")
            return last_build_info
        except Exception:
            last_build_info = {"started_timestamp": "2023-01-01 14:59:35", "build_status": "JOB NOT FOUND"}
            print(f"{self.name} - Last build info: {last_build_info}")
            return last_build_info

    def is_sla_violated(self, last_build_info: dict):
        last_build_date = datetime.datetime.strptime(last_build_info["started_timestamp"],
                                                     "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date = str(datetime.date.today())
        if current_timestamp > self.sla_time and (last_build_info["build_status"].upper() != "SUCCESS"
                                                  or last_build_date < current_date):
            return True
        else:
            return False
