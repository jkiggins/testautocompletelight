import datetime
from django.utils import timezone

def dict_has_keys(keys, dict):
    for key in keys:
        if not(key in dict):
            return False
    return True

class EventCreationFormValidator:

    @staticmethod
    def add_messages(form, error, help):
        for key in error:
            form.add_error(key, error[key])

        for key in help:
            form.fields[key].help_text = help[key]

    @staticmethod
    def startDateInXhoursFuture(form, x, error, help):
        if not dict_has_keys(['startTime'], form.cleaned_data):
            return True
        if form.cleaned_data['startTime'] - timezone.now() < datetime.timedelta(hours=x):
            EventCreationFormValidator.add_messages(form, error, help)
            return False
        return True

    @staticmethod
    def eventPositiveDuration(form, minutes, error, help):
        if not dict_has_keys(['startTime', 'endTime'], form.cleaned_data):
            return True

        if(form.cleaned_data['endTime'] - form.cleaned_data['startTime']) < datetime.timedelta(minutes=minutes):
            EventCreationFormValidator.add_messages(form, error, help)
            return False
        return True

    @staticmethod
    def eventDurationBounded(form, low, high, error, help):
        if not dict_has_keys(['duration'], form.cleaned_data):
            return True
        if not(low <= form.cleaned_data['duration'] <= high):
            EventCreationFormValidator.add_messages(form, error, help)
            return False
        return True

    @staticmethod
    def patientMatchesHospital(form, error, help):
        if not dict_has_keys(['patient', 'hospital'], form.cleaned_data):
            return True

        p = form.cleaned_data['patient']

        if p != None:
            if p.hospital != form.cleaned_data['hospital']:
                EventCreationFormValidator.add_messages(form, error, help)
                return False
        return True

    @staticmethod
    def eventNotConflictingType(form, appt_value, error, help):
        if not dict_has_keys(['patient', 'type'], form.cleaned_data):
            return True

        if (form.cleaned_data['patient'] != None) and (form.cleaned_data['type'] != '2'):
            EventCreationFormValidator.add_messages(form, error, help)
            return False
        return True