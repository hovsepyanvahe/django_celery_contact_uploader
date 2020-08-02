from celery import shared_task
from .models import Contact, TemporaryBlockedContact, File
from celery_progress.backend import ProgressRecorder
from time import sleep


@shared_task(bind=True)
def temporary_block_contact(self, list_of_valid_contacts):
    for contact_dict in list_of_valid_contacts:
        temp_block = TemporaryBlockedContact()
        temp_block.email = contact_dict.get('Email Address')
        temp_block.phone = contact_dict.get('Phone Number')
        temp_block.save()
    sleep(15)
    for contact_dict in list_of_valid_contacts:
        temp_block = TemporaryBlockedContact.objects.get(email=contact_dict.get('Email Address'),
                                                         phone=contact_dict.get('Phone Number'))
        temp_block.delete()


@shared_task(bind=True)
def process_contacts(self, list_of_valid_contacts):
    progress_recorder = ProgressRecorder(self)
    progress_length = len(list_of_valid_contacts)

    for counter, contact_dict in enumerate(list_of_valid_contacts):
        contact = Contact()
        contact.name = contact_dict.get('Name')
        contact.phone = contact_dict.get('Phone Number')
        contact.email = contact_dict.get('Email Address')
        contact.save()
        progress_recorder.set_progress(counter, progress_length,
                                       'Thank you for uploading your contacts, the upload is underway')
