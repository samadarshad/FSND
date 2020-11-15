from models import db

# e.g. groupClassBy(Venue, 'venues', 'city', 'state')
def groupClassBy(dbClass, dbClassDictKeyName, *argv):
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