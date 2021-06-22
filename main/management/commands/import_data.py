import csv, os
from collections import Counter
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = 'Import products in BookStore'

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=str)
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        self.stdout.write('Importing products')
        c = Counter()
        csvfile_path = settings.BASE_DIR / options['csvfile']

        if not os.path.exists(csvfile_path):
            self.stdout.write(f"The file: '{csvfile_path}' does not exist")
            return

        images_dir = settings.BASE_DIR / options['image_basedir']
        if not os.path.exists(images_dir):
            self.stdout.write(f"The directory: '{images_dir}' does not exist")
            return

        with open(csvfile_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product, created = models.Product.objects.get_or_create(
                    name=row['name'], price=row['price']
                )
                product.description = row['description']
                product.slug = slugify(row['name'])

                image_path = images_dir / row['image_filename']
                if not os.path.exists(image_path):
                    self.stdout.write(f"Could not create product '{product.name}' and its image: '{image_path}'")
                    self.stdout.write(f"The image: '{image_path}' does not exist")
                    product.delete()
                    continue

                for import_tag in row['tags'].split("|"):
                    tag, tag_created = models.ProductTag.objects.get_or_create(name=import_tag)
                    product.tags.add(tag)
                    c['tags'] += 1
                    if tag_created:
                        c['tags_created'] += 1

                if created:
                    with open(images_dir / row['image_filename'], 'rb') as f:
                        image = models.ProductImage(
                            product=product,
                            image=ImageFile(f, name=row['image_filename'])
                        )
                        image.save()
                        c['images_created'] += 1
                product.save()
                c['products'] += 1
                if created:
                    c['products_created'] += 1
        self.stdout.write(
            "Products processed=%d (created=%d)"
            % (c['products'], c['products_created'])
        )
        self.stdout.write(
            "Tags processed=%d (created=%d)"
            % (c['tags'], c['tags_created'])
        )
        self.stdout.write("Images created=%d" % c['images_created'])
