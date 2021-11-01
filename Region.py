
# Trying to import data into database using mongoengine
# https://www.tutorialspoint.com/mongoengine/mongoengine_document_class.htm
from mongoengine import *
import pandas as pd

class Region(DynamicDocument):
    type = StringField()
    name = StringField()
    region_code = StringField()
    population = DictField(DictField())

    #########################
    # Second dataset variables
    #########################
    facilities = DictField()


    def __init__(self, name, *args, **values):
        super().__init__(*args, **values)
        self.name = name


def insert_population_csv(file_path, encoding):
    # Loading csv to pandas dataframe
    df = pd.read_csv(file_path, encoding=encoding)

    print(df.sort_values(['vuzemi_txt', 'casref_do', 'vek_txt']).head(10))
    print('Regions to save: '+ str(df['vuzemi_txt'].nunique()))

    # Creating collection
    region = Region('')
    pop_dict = {}
    first_iteration = True

    # Iterate trough dataframe and create collections
    for index, row in df.sort_values(['vuzemi_txt', 'casref_do', 'vek_txt']).iterrows():

        # Init first region in first iteration
        if first_iteration :
            region.name = row['vuzemi_txt']
            first_iteration = False

       # When region changes save the values and init new region
        if region.name != row['vuzemi_txt']:
            region.population = pop_dict
            region.save()
            region = Region(row['vuzemi_txt'])


        # key for specific value -- age + sex is the key
        # We replace some character for better formatting
        my_key = str(row['vek_txt'])[0:8].replace(' až ', '-').replace(' (','').replace('v','').replace('nan','Sum') \
                 + ' ' + str(row['pohlavi_txt']).replace('nan','')

        # Creating population dict
        if row['casref_do'] not in pop_dict.keys():
            pop_dict[row['casref_do']] = {}
            pop_dict[row['casref_do']][my_key] = row['hodnota']
        else:
            pop_dict[row['casref_do']][my_key] = row['hodnota']

    # Save the last region after finishing iteration
    region.population = pop_dict
    region.save()
    print(pop_dict['2010-12-31'])






