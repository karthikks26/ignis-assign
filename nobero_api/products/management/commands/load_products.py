# products/management/commands/load_products.py

from django.core.management.base import BaseCommand
import json
from products.models import Product

class Command(BaseCommand):
    help = 'Load product data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        file_path = options['file']
        with open(file_path) as f:
            products = json.load(f)
            for product in products:
                Product.objects.create(**product)
        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))
