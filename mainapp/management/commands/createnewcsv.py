import numpy
import pandas as pd


class Command(BaseCommand):

    help = 'check which objects already in db'

    def handle(self, *args, **options):

        def createnewcsv(oldcsv):

            reader = pd.read_csv(dataframe, sep=';')
            format_list = ["LP+CD", "LP", "2LP",
                           "3LP", "12'", "LP+CD+7'", "7'"]
            newreader = reader.fillna(" ")
            reader_LP = newreader[newreader.FORMAT.isin(format_list)]
            reader_LP.to_csv("lpfile.csv")

        creatnewcsv("mainapp/management/entertainmenttrad136.csv")
