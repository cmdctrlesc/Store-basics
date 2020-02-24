from django.core.management.base import BaseCommand, CommandError
import numpy
import pandas as pd
from mainapp.models import Record, Label, Artist
from urllib.request import urlopen
import json
from .apimodule import wikilabelsearch, wikiartistsearch, wikititlesearch, discogspicsearch, youtubesearch


class Command(BaseCommand):

    help = 'create objects in db using pandas'

    def add_arguments(self, parser):
        parser.add_argument("start_of_chunk", type=int)

        parser.add_argument("len_of_chunk", type=int)

    def handle(self, *args, **options):
        start_of_chunk = options["start_of_chunk"]
        len_of_chunk = options["len_of_chunk"]

        def addtodb(dataframe, start_of_chunk, len_of_chunk):

            objectsindb = len(Record.objects.all())

            assert start_of_chunk >= objectsindb, "To avoid adding duplicates to the database, your start_of_chunk argument should be {}".format(
                objectsindb)

            reader = pd.read_csv(dataframe)

            id_lst = reader.iloc[start_of_chunk:len_of_chunk]['ID']
            artist_lst = list((reader.iloc[start_of_chunk:len_of_chunk]['ARTIST']).apply(
                lambda x: x.upper()))
            title_lst = list((reader.iloc[start_of_chunk:len_of_chunk]['TITLE']).apply(
                lambda x: x.upper()))
            ean_lst = list(reader.iloc[start_of_chunk:len_of_chunk]['BARCODE'])
            unit_lst = list(reader.iloc[start_of_chunk:len_of_chunk]['UNIT'])
            format_lst = list(
                reader.iloc[start_of_chunk:len_of_chunk]['FORMAT'])
            label_lst = list((reader.iloc[start_of_chunk:len_of_chunk]['LABEL']).apply(
                lambda x: x.upper()))
            price_lst = list(reader.iloc[start_of_chunk:len_of_chunk]['PRICE'])
            precision_lst = list(
                reader.iloc[start_of_chunk:len_of_chunk]['PRECISION'])
            delivery_lst = list(
                reader.iloc[start_of_chunk:len_of_chunk]['DELIVERY'])
            stock_lst = list(reader.iloc[start_of_chunk:len_of_chunk]['STOCK'])
            date_lst = list(reader.iloc[start_of_chunk:len_of_chunk]['DATE'])

            labelstoadd = []

            for label in set(label_lst):
                if not Label.objects.filter(name=label):
                    labelstoadd.append(label)
                else:
                    pass

            labelsearchresults = wikilabelsearch(labelstoadd)
            labeldescription_lst = labelsearchresults[0]
            labellink_lst = labelsearchresults[1]

            labelswithinfo = []

            for a, b, c in zip(labelstoadd, labeldescription_lst, labellink_lst):

                labelswithinfo.append(
                    Label(name=a, wikiinfo=b, wikiinfolink=c))

            Label.objects.bulk_create(labelswithinfo)

            artiststoadd = []

            for artist in set(artist_lst):

                if not Artist.objects.filter(name=artist):
                    artiststoadd.append(artist)
                else:
                    pass

            artistsearchresults = wikiartistsearch(artiststoadd)
            artistdescription_lst = artistsearchresults[0]
            artistlink_lst = artistsearchresults[1]

            artistswithinfo = []

            for a, b, c in zip(artiststoadd, artistdescription_lst, artistlink_lst):

                artistswithinfo.append(
                    Artist(name=a, wikiinfo=b, wikiinfolink=c))

            Artist.objects.bulk_create(artistswithinfo)

            titlesearchresults = wikititlesearch(title_lst, artist_lst)
            wikiinfo_lst = titlesearchresults[0]
            wikilink_lst = titlesearchresults[1]
            discogspic_lst = discogspicsearch(
                artist_lst, title_lst, id_lst, ean_lst)
            ytlink_lst = youtubesearch(artist_lst, title_lst)

            recordstoadd = []
            for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p in zip(id_lst, artist_lst, title_lst, ean_lst, unit_lst, format_lst, label_lst, price_lst, precision_lst, delivery_lst, stock_lst, date_lst, wikiinfo_lst, wikilink_lst, discogspic_lst, ytlink_lst):

                recordstoadd.append(Record(recordid=a, artist=Artist.objects.get(name=b), title=c, barcode=d, unit=e, recordformat=f, label=Label.objects.get(name=g),
                                           price=h, precision=i, delivery=j, stock=k, date=l, wikiinfo=m, wikilink=n, discogspicurl=o, ytlink=p))

            Record.objects.bulk_create(recordstoadd)

        listsfordb = addtodb("mainapp/management/newfile.csv",
                             start_of_chunk, len_of_chunk)
