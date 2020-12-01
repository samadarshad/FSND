from datetime import timedelta


default_availability_slot_duration_days=1
default_booking_slot_duration_days=0.5

#######################

default_availability_slot_duration = timedelta(days=default_availability_slot_duration_days)
default_booking_slot_duration = timedelta(days=default_booking_slot_duration_days)

placeholder_booking='Defaults to Start Time + ' + str(default_booking_slot_duration_days) + ' days'
placeholder_availability='Defaults to Start Time + ' + str(default_availability_slot_duration_days) + ' days'