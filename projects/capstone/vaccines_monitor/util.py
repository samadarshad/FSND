import os
import config
from flask import abort
import inspect

email_prefix = os.getenv('PATIENT_EMAIL_PREFIX')
email_suffix = os.getenv('PATIENT_EMAIL_SUFFIX')
patient_password = os.getenv('PATIENT_PASSWORD')


def formEmail(id):
    return email_prefix + str(id) + email_suffix


def formPassword():
    return patient_password


def getInstanceOrAbort(Class, id):
    instance = Class.query.get(id)
    if not instance:
        abort(404)
    return instance


def deleteInstanceOrAbort(Class, id):
    obj = getInstanceOrAbort(Class, id)
    try:
        obj.delete()
    except Exception:
        abort(422)


def populateObjectFromJson(obj, body):
    attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
    attributes = [a[0] for a in attributes if not(a[0].startswith('_'))]
    for a in attributes:
        if a in body:
            setattr(obj, a, body.get(a))
    return obj


def getPaginatedTable(Table, page, items_per_page):
    items = Table.query.order_by(Table.id).paginate(
        page, items_per_page, error_out=False)
    items_formatted = [t.format() for t in items.items]
    total_number = len(Table.query.all())

    return {'items': items_formatted, 'total_number': total_number}
