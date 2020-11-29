from datetime import datetime
import sqlalchemy.sql.sqltypes
import inspect
import dateutil.parser
import babel
import re

def splitSearchTerm(searchTerm):
  return re.split('; |, |\*|\n',searchTerm)

def groupClassBy(db, dbClass, dbClassDictKeyName, *argv):
  listOfAttributes = []
  for arg in argv:
    listOfAttributes.append(getattr(dbClass, arg))
  groupedClass = db.session.query(*listOfAttributes).group_by(*listOfAttributes).all()

  groupedClassDict = []

  for vals in groupedClass:
    keyvalues = {}
    for arg, val in zip(argv, vals):
      keyvalues[arg] = val
    groupedClassDict.append(keyvalues)
  
  groupedClassDict_withClass = []  

  for r in groupedClassDict:
    filterings = [(attr==r[arg]) for attr, arg in zip(listOfAttributes, argv)]
    selectedvenues = dbClass.query.filter(*filterings).all()
    groupedClassDict_withClass.append({**r, **{dbClassDictKeyName: selectedvenues}})

  return groupedClassDict_withClass

def populateObjectFromRequest(obj, request):
  attributes = inspect.getmembers(obj, lambda a:not(inspect.isroutine(a)))
  attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
  for a in attributes:
    if a in request.form:
      if isinstance(getattr(type(obj), a).type, sqlalchemy.sql.sqltypes.ARRAY):
        setattr(obj, a, request.form.getlist(a))
      else:
        setattr(obj, a, request.form[a])
  return obj

def setFormDefaultValues(form, obj):
  attributes = inspect.getmembers(form, lambda a:not(inspect.isroutine(a)))
  attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
  for a in attributes:
    if hasattr(obj, a):
      setattr(getattr(form, a), "default", getattr(obj, a))
  form.process()

def format_datetime(value, format='medium'):  
  date = None
  if type(value) is str:
    date = dateutil.parser.parse(value)
  elif type(value) is datetime:
    date = value
  else:
    return "Error: invalid input to format_datetime"

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)