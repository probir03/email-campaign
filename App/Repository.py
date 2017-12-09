import datetime
import env
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from app import db

def filterByAttribute(modelName, filterKeys):
    return modelName.query.get(filterKeys)

def filerByRawPaginated(query, item=25, page=1):
	return query.paginate(page=int(page), per_page=int(item), error_out=False)

def filterByAttributePaginated(modelName, filterKeys={}, expressions=None, item=25, page=1, sortBy={'created_at':'desc'}):
	orderBy = []
	for column, order in sortBy.iteritems() :
		orderBy.append(getattr(getattr(modelName, column), order)())

	if expressions is not None:
		print expressions
		return modelName.query.filter(expressions['query']).filter_by(**filterKeys).order_by(*orderBy).paginate(page=int(page), per_page=int(item), error_out=False)
	return modelName.query.filter_by(**filterKeys).order_by(*orderBy).paginate(page=int(page), per_page=int(item), error_out=False)

def authenticate(modelName, access_token):
    return modelName.query.filter(access_token=access_token, expires_at__gte=datetime.datetime.now())

def authenticate_admin(modelName, user_id):
    return modelName.query.filter(id=user_id)

def filter_attribute(modelName, filterKeys):
    return modelName.query.filter_by(**filterKeys)

def update(modelName, filterKeys, updateWith):
	row = db.session.query(modelName).filter_by(**filterKeys).update(updateWith) 
	db.session.commit()
	return row

def fetchAll(modelName):
    return modelName.query.all()

def fetchSelect(modelName, select_params):
	from sqlalchemy.orm import load_only
	# return modelName.query.options(load_only(select_params)).all()
	return modelName.query.options(load_only(*select_params)).all()

def store(modelName, values):
	modelInstance = modelName(**values)
	db.session.add(modelInstance)
	db.session.commit()
	return modelInstance

def delete(modelName, filterKeys):
	rows = db.session.query(modelName).filter_by(**filterKeys).delete()
	# print dd.delete(synchronize_session = False)
	db.session.commit()
	return rows








