import Region as reg
import database_driver as driver


csv_file_path_population = r'Dataset/130142-21data043021.csv'
csv_file_path_facilities = r'Dataset/export-sluzby-2021-10.csv'

driver.connect_to_db()
reg.delete_existing()
reg.insert_population_csv(csv_file_path_population,'utf8', csv_file_path_facilities, 'cp1250')








