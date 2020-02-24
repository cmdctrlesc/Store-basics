from django.core.management.base import BaseCommand, CommandError
import numpy
import pandas as pd
from firstapp.models import Record


class Command(BaseCommand):

    help = 'check which objects already in db'

    def handle(self, *args, **options):

        def updatestock(csvfile):

            id_old = []
            stock_old = []
            stock_zero = []
            newrows = []

            reader = pd.read_csv(csvfile, sep=';')
            format_list = ["LP+CD", "LP", "2LP",
                           "3LP", "12'", "LP+CD+7'", "7'"]
            newreader = reader.fillna(" ")
            reader_LP = newreader[newreader.FORMAT.isin(format_list)]
            id_lst = reader_LP['ID']
            stock_lst = reader_LP['STOCK']

            for idnum, stock in zip(id_lst, stock_lst):

                if Record.objects.filter(recordid=idnum).exists():

                    id_old.append(idnum)
                    stock_old.append(stock)

                else:
                    newrows.append(id_lst[id_lst == idnum].index[0])
                    stock_zero.append(idnum)

            series = [reader.iloc[row] for row in newrows]

            newdf = pd.DataFrame(series)
            # newdf.to_csv("itemsnotindb.csv")

            for a, b in zip(id_old, stock_old):
                Record.objects.filter(recordid=a).update(stock=b)

            print(len(id_old))
            print(len(stock_old))

            for c in stock_zero:
                Record.objects.filter(recordid=c).update(stock=0)

        updatestock(csvfile="firstapp/management/entertainmenttrad136new.csv")
