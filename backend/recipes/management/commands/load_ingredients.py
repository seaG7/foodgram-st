import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, '..', 'data', 'ingredients.json')

        try:
            with open(data_path, encoding='utf-8') as file:
                data = json.load(file)
                ingredients_to_create = []
                for item in data:
                    ingredients_to_create.append(
                        Ingredient(
                            name=item['name'],
                            measurement_unit=item['measurement_unit']
                        )
                    )
                Ingredient.objects.bulk_create(ingredients_to_create)
            
            self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены!'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл не найден по пути: {data_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
