from job import Job
from notifier import Notifier
from os import getenv
from time import sleep

import datetime

# ENV VARS NEEDED: JENKINS_HOST, JENKINS_USERNAME, JENKINS_PASSWORD, MONITOR_START_HOUR, VERIFICATION_END_HOUR,
# CHECK_INTERVAL, SLA_CONFIG_PATH, SLA_INCREASE, TWILIO_SID, TWILIO_AUTH_TOKEN


def main():
    monitor_start_hour = int(getenv("MONITOR_START_HOUR", default=0))
    monitor_end_hour = int(getenv("MONITOR_END_HOUR", default=23))
    # check_interval = 60 * int(getenv("CHECK_INTERVAL", default=10))
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    violation_list = []
    if monitor_start_hour <= datetime.datetime.now().hour <= monitor_end_hour:
        print(f"STARTING A NEW VERIFICATION AT: {current_timestamp}")
        try:
            jobs = Job.read_from_yaml()
            qty_sla_violated = 0
            for job in jobs:
                last_build_info = job.get_job_last_build_info()
                if job.is_sla_violated(last_build_info=last_build_info):
                    qty_sla_violated = qty_sla_violated + 1
                    violation_list.append(job.name)

            if qty_sla_violated > 0:
                print(f"SLA violated quantity {qty_sla_violated}, calling pager")
                print(violation_list)
                notifier = Notifier()
                notifier.call()

            # sleep(check_interval)
        except Exception:
            print("The python code is broken, calling to check")
            notifier = Notifier()
            notifier.call()
            # sleep(check_interval)
    else:
        print(f"The hour is not between {monitor_start_hour} and {monitor_end_hour}, waiting the next validation "
              f"window")
        # sleep(check_interval)


if __name__ == "__main__":
    main()
