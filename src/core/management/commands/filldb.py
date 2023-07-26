from random import choice

from django.core.management.base import BaseCommand

from core.factories import RegionFactory
from core.models import Region
from bot.factories import (CoordinatorFactory,
                           FundProgramFactory,
                           QuestionFactory)
from bot.models import (Coordinator,
                        FundProgram,
                        Question)


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Question.objects.all().delete()
        FundProgram.objects.all().delete()
        Coordinator.objects.all().delete()
        Region.objects.all().delete()
        self.stdout.write("Creating new data...")
        regions = []
        for _ in range(5):
            while True:
                try:
                    region = RegionFactory()
                except Exception:
                    continue
                else:
                    regions.append(region)
                    break

        for _ in range(5):
            region = choice(regions)
            CoordinatorFactory(region=region)
            fund_program = FundProgramFactory()
            fund_program.regions.add(region)
            question = QuestionFactory()
            question.regions.add(region)
