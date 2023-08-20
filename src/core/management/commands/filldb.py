from random import choice, randint, sample

from django.core.management.base import BaseCommand

from bot.factories import (
    CoordinatorFactory,
    FundProgramFactory,
    QuestionFactory,
)
from bot.models import Coordinator, FundProgram, HelpTypes, Question
from core.factories import RegionFactory
from core.models import Region

REGION_COUNT = int(input("Необходимое количество регионов: "))
PROGRAM_COUNT = int(input("Необходимое количество программ: "))
QUESTION_TYPE_LAW_COUNT = int(
    input("Необходимое количество вопросов юридической помощи: ")
)
QUESTION_TYPE_SOCIAL_COUNT = int(
    input("Необходимое количество вопросов социальной помощи: ")
)
QUESTION_TYPE_MENTAL_COUNT = int(
    input("Необходимое количество вопросов психологической помощи: ")
)


class Command(BaseCommand):
    """Generating test data and filling the database with it."""

    help = "Fill the database with test data"

    def handle(self, *args, **kwargs):
        """Clean up and fill in the model data."""

        self.stdout.write("Deleting old data...")
        Question.objects.all().delete()
        FundProgram.objects.all().delete()
        Coordinator.objects.all().delete()
        Region.objects.all().delete()
        self.stdout.write("Creating new data...")

        for _ in range(REGION_COUNT):
            while len(Region.objects.all()) < REGION_COUNT:
                region = RegionFactory()

        regions = list(Region.objects.all())

        for _ in range(REGION_COUNT):
            CoordinatorFactory()

        for _ in range(PROGRAM_COUNT):
            region = choice(regions)
            fund_program = FundProgramFactory()
            fund_program.regions.add(region)

        for _ in range(QUESTION_TYPE_LAW_COUNT):
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)

        for _ in range(QUESTION_TYPE_SOCIAL_COUNT):
            social_type = HelpTypes.SOCIAL_ASSISTANCE
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)
            question.question_type = social_type
            question.save()

        for _ in range(QUESTION_TYPE_MENTAL_COUNT):
            mental_type = HelpTypes.PSYCHOLOGICAL_ASSISTANCE
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)
            question.question_type = mental_type
            question.save()
