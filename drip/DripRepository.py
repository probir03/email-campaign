import os, datetime
from App.Repository import *
from helpers import generate_unique_code, hash_password
# from Orgs.models import OrganisationUser, OrgTypeOrg, OrgTypeOrgUser
# from models import User


##
# AuthRepository - For all database transactions
##
class DripRepository():

    ##
    # To Store the data
    ##
    def store(self, model, data):
        result = store(model, data)
        return result

    def update(self, model, filterBy, data):
        result = update(model, filterBy, data)
        return result

    def fech_by_user(self, model, filter_by):
        return filter_attribute(model, filter_by).all()

    def fetch_all(self, model):
        result = fetchAll(model)
        return result

    def filter_attribute(self, model, findBy):
        result = filter_attribute(model, findBy).first()
        return result

    def delete(self, model, findBy):
        result = delete(model, findBy)
        return result
