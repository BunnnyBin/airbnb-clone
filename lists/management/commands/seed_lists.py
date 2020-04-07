import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


class Command(BaseCommand):
    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(list_models.List, number, {
            "user": lambda x: random.choice(users),
        })
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)] #room의 범위를 한정한다.
            list_model.rooms.add(*to_add) # room과 list는 다대다관계
                                          # to_add - 쿼리셋(배열) -> * : 배열안의 요소들
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
