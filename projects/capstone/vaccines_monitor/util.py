import os
import config
from flask import abort

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