
import Database_driver as driver
import pandas as pd
import numpy as np
import Region as rg


csv_file_path_population = r'Dataset/130142-21data043021.csv'
csv_file_path_facilities = r'Dataset/export-sluzby-2021-10.csv'


def delete_existing():
    collection = rg.Region.objects()
    collection.delete()


def get_domain_dict(df_fac, reg_name, domains_list):

    domain_dict = {}
    df_domain_region = df_fac[df_fac['Okres'] == reg_name]
    df_domain_region['OborPece'] = df_domain_region['OborPece'].fillna('neznamy')
    for dom in domains_list:
        domain_dict[dom] = {}

    for idx, row_fac in df_domain_region.iterrows():
        facility_dict = {}
        facility_dict['NazevCely'] = row_fac['NazevCely']
        facility_dict['DatumZahajeniCinnosti'] = row_fac['DatumZahajeniCinnosti']
        facility_dict['Obec'] = row_fac['Obec']
        facility_dict['Ulice'] = row_fac['Ulice']
        facility_dict['FormaPece'] = row_fac['FormaPece']
        facility_dict['DruhPece'] = row_fac['DruhPece']
        facility_dict['GPS'] = row_fac['GPS']

        domain_dict[row_fac['OborPece'].replace('nan', 'neznamy')][
            str(idx)] = facility_dict

    return domain_dict

def insert_population_csv(file_path_population, encoding_population, file_path_facilities, encoding_facilities):
    # Loading csv to pandas dataframe
    df_pop = pd.read_csv(file_path_population, encoding=encoding_population)
    df_fac = pd.read_csv(file_path_facilities, encoding=encoding_facilities, delimiter=';', header=0)

    print(df_pop.sort_values(['vuzemi_txt', 'casref_do', 'vek_txt']).head(10))
    print('Regions to save: '+ str(df_pop['vuzemi_txt'].nunique()))

    df_fac = df_fac.sort_values(['Okres', 'OborPece'])
    print(df_fac[['Okres', 'OborPece']].head(10))
    print('Domains to save: ' + str(df_fac['OborPece'].nunique(10)))

    # Creating collection
    region = rg.Region('')
    pop_dict = {}
    first_iteration = True
    # Creating list of domains
    domains_list = ['neznamy' if x is np.nan else x for x in df_fac['OborPece'].unique()]

    # Iterate trough dataframe and create collections
    for index, row in df_pop.sort_values(['vuzemi_txt', 'casref_do', 'vek_txt']).iterrows():
        # Init first region in first iteration
        if first_iteration:
            region.name = row['vuzemi_txt']
            first_iteration = False

       # When region changes save the values and init new region
        if region.name != row['vuzemi_txt']:
            region.population = pop_dict

            # Iterate over all facilities in region and add to domain
            region.domain = get_domain_dict(df_fac, region.name, domains_list)

            print("Inserting region: ", region.name)
            region.save()
            region = rg.Region(row['vuzemi_txt'])

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

        #creating domain dict



    # Save the last region after finishing iteration
    region.population = pop_dict

    # Iterate over all facilities in region and add to domain
    region.domain = get_domain_dict(df_fac, region.name, domains_list)

    region.save()


driver.connect_to_db()
delete_existing()
insert_population_csv(csv_file_path_population,'utf8', csv_file_path_facilities, 'cp1250')





