from django.core.management.base import BaseCommand, CommandError
from core.models import Person, Property

from random import randrange, choice

import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Generate random data for `Person` and `Property` models'

    def handle(self, *args, **options):
        url = 'https://www.fakenamegenerator.com/gen-random-au-au.php'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        for idx in range(3):
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find("div", {"class": "address"})

            full_name = data.find("h3").text.split(' ')
            first_name = full_name[0]
            last_name = full_name[-1]

            p = Person.objects.create(
                first_name = first_name,
                last_name = last_name,
                age = randrange(16, 60)
            )

            self.stdout.write(str(p))

        all_people = Person.objects.all()
        for idx in range(20):
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find("div", {"class": "address"})

            full_address = data.find("div").contents
            street = full_address[0].strip()
            suburb, state, postcode = full_address[-1].strip().rsplit(' ', 2)

            p = Property.objects.create(
                street = street,
                suburb = suburb,
                state = state,
                postcode = postcode,
                value = randrange(100000, 2000000),
                owner = choice(all_people)
            )

            self.stdout.write(str(p))
