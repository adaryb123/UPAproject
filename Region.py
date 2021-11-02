
# Trying to import data into database using mongoengine
# https://www.tutorialspoint.com/mongoengine/mongoengine_document_class.htm
from mongoengine import *


class Region(DynamicDocument):
    type = StringField()
    name = StringField()
    region_code = StringField()
    population = DictField(DictField())
    ############################
    # Second dataset variables #
    ############################
    domain = DictField(DictField(DictField()))

    def __init__(self, name, *args, **values):
        super().__init__(*args, **values)
        self.name = name









