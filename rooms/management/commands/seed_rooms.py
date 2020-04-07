import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(room_models.Room, number, {
            # faker : seeder는 필드와 상관없이 아무관계없는 데이터를 넣지만 faker는 address,city 등에 맞춰서 데이터를 생성해준다.
            "name": lambda x: seeder.faker.address(),
            # 랜덤 호스트, 룸타입을 뽑는 함수 - 일대다 관계
            "host": lambda x: random.choice(all_users),
            "room_type": lambda x: random.choice(room_types),
            # 점수가 음수로 나오지 않게 하는 함수
            "guests": lambda x: random.randint(0, 20),
            "price": lambda x: random.randint(0, 5),
            "beds": lambda x: random.randint(0, 5),
            "bedrooms": lambda x: random.randint(0, 5),
            "baths": lambda x: random.randint(0, 5),
        })
        created_photos = seeder.execute()
        print(list(created_photos.values()))  # 생성된 room의 pk 출력!!!
        created_clean = flatten(list(created_photos.values()))  # flatten : 이중 리스트를 깔끔하게 벗겨주는 것
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            amenities = room_models.Amenity.objects.all()
            facilities = room_models.Facility.objects.all()
            rules = room_models.HouseRule.objects.all()
            # Photo - 여러개 생성
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    # file url
                    file=f"room_photos/{random.randint(1, 10)}.jpg",
                )
            # Amenities, Facility, Houserule - 다대다 관계
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)  # "다대다 관계"일때 모델 추가하는 방법 - create()와 다르게
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
