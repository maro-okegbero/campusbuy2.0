from abc import ABC

# from bunch import bunchify
from django.core.management.base import BaseCommand, CommandError

try:
    from munch import munchify
except ModuleNotFoundError as e:
    raise CommandError("Install the requirements.txt file")

from app.models import School


class Command(BaseCommand, ABC):
    help = "Loads universities to the database"

    def handle(self, *args, **options):
        data = [

            dict(
                name="University Of Benin",
                state="Edo",
                alias="Uniben"),

            dict(
                name="University Of PortHarcourt",
                state="Rivers",
                alias="Uniport"
            ),
            dict(
                name="University Of Lagos",
                state="Lagos",
                alias="Unilag"
            ),

        ]
        for d in data:
            b = munchify(d)
            try:
                School.objects.create(name=b.name, alias=b.alias, state=b.state)
                self.stdout.write(self.style.SUCCESS(f'{b.name} has been loaded successfully'))
            except Exception as e:
                print(f"There was an exception =====>>>>>> {e}")
                continue
        self.stdout.write(self.style.SUCCESS('Schools have been loaded successfully'))


