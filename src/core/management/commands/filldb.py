from random import choice, randint, sample

from django.core.management.base import BaseCommand
from tqdm import tqdm

from bot.factories import (
    CoordinatorFactory,
    FundProgramFactory,
    QuestionFactory,
)
from bot.models import Coordinator, FundProgram, HelpTypes, Question
from core.factories import RegionFactory
from core.models import Region

PROGRESS_BAR_CONFIG = {"ncols": 100, "colour": "green"}

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

        for _ in tqdm(
            range(REGION_COUNT), desc="Creating regions", **PROGRESS_BAR_CONFIG
        ):
            while len(Region.objects.all()) < REGION_COUNT:
                region = RegionFactory()

        regions = list(Region.objects.all())

        for _ in tqdm(
            range(REGION_COUNT),
            desc="Creating coordinators",
            **PROGRESS_BAR_CONFIG,
        ):
            CoordinatorFactory()

        for _ in tqdm(
            range(PROGRAM_COUNT),
            desc="Creating programs",
            **PROGRESS_BAR_CONFIG,
        ):
            region = choice(regions)
            fund_program = FundProgramFactory()
            fund_program.regions.add(region)

        for _ in tqdm(
            range(QUESTION_TYPE_LAW_COUNT),
            desc="Creating law questions",
            **PROGRESS_BAR_CONFIG,
        ):
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)

        for _ in tqdm(
            range(QUESTION_TYPE_SOCIAL_COUNT),
            desc="Creating social questions",
            **PROGRESS_BAR_CONFIG,
        ):
            social_type = HelpTypes.SOCIAL_ASSISTANCE
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)
            question.question_type = social_type
            question.save()

        for _ in tqdm(
            range(QUESTION_TYPE_MENTAL_COUNT),
            desc="Creating mental questions",
            **PROGRESS_BAR_CONFIG,
        ):
            mental_type = HelpTypes.PSYCHOLOGICAL_ASSISTANCE
            regions_count = randint(1, len(regions))
            regions_for_question = sample(regions, k=regions_count)
            question = QuestionFactory()
            for region in regions_for_question:
                question.regions.add(region)
            question.question_type = mental_type
            question.save()
