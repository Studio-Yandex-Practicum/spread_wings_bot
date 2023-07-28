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

REGION_COUNT = int(input("Необходимое количество регионов: "))
COORDINATOR_COUNT = int(input("Необходимое количество координаторов: "))
PROGRAM_COUNT = int(input("Необходимое количество программ: "))
QUESTION_COUNT = int(input("Необходимое количество вопросов: "))


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
        for _ in range(REGION_COUNT):
            while True:
                try:
                    region = RegionFactory()
                except Exception:
                    continue
                else:
                    regions.append(region)
                    break

        for _ in range(COORDINATOR_COUNT):
            region = choice(regions)
            CoordinatorFactory(region=region)

        for _ in range(PROGRAM_COUNT):
            region = choice(regions)
            fund_program = FundProgramFactory()
            fund_program.regions.add(region)

        for _ in range(QUESTION_COUNT):
            region = choice(regions)
            question = QuestionFactory()
            question.regions.add(region)
