from datetime import timedelta

from django_cron import CronJobBase, Schedule

from django.utils import timezone
from .models import Bidder
from conf.settings import UNBLOCK_TIME


class UnblockBidders(CronJobBase):

    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bidders_cleaner'

    def do(self):

        bidders = Bidder.objects.filter(blocked=True)

        unban_list = [
            b for b in bidders if timezone.now() -
            b.last_fail >= timedelta(hours=UNBLOCK_TIME)
        ]

        for user in unban_list:
            user.blocked = False
            user.fails_count = 0
            user.save()
