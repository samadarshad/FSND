import os
import config

email_prefix = os.getenv('PATIENT_EMAIL_PREFIX')
email_suffix = os.getenv('PATIENT_EMAIL_SUFFIX')
patient_password = os.getenv('PATIENT_PASSWORD')


def formEmail(id):
    return email_prefix + str(id) + email_suffix


def formPassword():
    return patient_password
