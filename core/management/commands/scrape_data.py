from django.core.management.base import BaseCommand, CommandError

from ._food_data_scraper import FoodDataScraper
from game.models import Consumable, Variant

class Command(BaseCommand):

    @FoodDataScraper.for_parsed_files
    def get_data(self, data):
        if Consumable.objects.filter(name=data['name']).exists():
            return

        consumable = Consumable()
        consumable.name = data['name']
        consumable.sources = data['sources']
        consumable.save()

        for variant_data in data['variants']:
            variant = Variant()
            variant.storage_type = variant_data['storage_type']
            variant.avg_retail_price = variant_data['avg_retail_price'][0]
            variant.retail_price_measurement = variant_data['avg_retail_price'][1]
            variant.prep_yield_factor = variant_data['prep_yield_factor']
            variant.size_of_cup_equivalent = variant_data['size_of_cup_eq'][0]
            variant.size_of_cup_eq_measurement = variant_data['size_of_cup_eq'][1]
            variant.avg_price_per_cup = variant_data['avg_price_per_cup']
            variant.addendum = variant_data['addendum']
            variant.consumable = consumable
            variant.save()

    def handle(self, *args, **options):
        print('Do you wish to delete and repopulate the db with newly scraped data?')
        print('Yes = delete and repopulate data')
        confirmation = input().strip()

        if confirmation != 'Yes':
            print('Input was not Yes. No data was added to the db.')
            quit()

        Consumable.objects.all().delete()
        self.get_data()
