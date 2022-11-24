#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from common.read_yaml import read_config
from task.update_alidns import update_new_record


def start_job():
    scheduler = BlockingScheduler()

    scheduler.add_job(func=update_new_record, trigger=read_config('job')['trigger_type'],
                      minutes=read_config('job')['schedule_time']['minutes'], name=read_config('job')['name'])

    try:
        scheduler.start()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    start_job()
