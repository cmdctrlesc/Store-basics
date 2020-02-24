from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Record
from django.template.defaultfilters import slugify


class Command(BaseCommand):

    help = 'check which objects already in db'

    def handle(self, *args, **options):

        def updateslug():
            allrecords = Record.objects.all()
            for record in allrecords:
                if not record.slug:
                    record.slug = '-'.join((slugify(record.artist.name),
                                            slugify(record.title)))
                    record.save()

                else:
                    pass

        updateslug()
