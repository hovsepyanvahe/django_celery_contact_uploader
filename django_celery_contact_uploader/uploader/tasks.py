from celery import shared_task
from .models import Contact, TemporaryBlockedContact, File
from celery_progress.backend import ProgressRecorder
from time import sleep


@shared_task(bind=True)
def temporary_block_contact(self, contact_dict):
    temp_block = TemporaryBlockedContact()
    temp_block.email = contact_dict.get('Email Address')
    temp_block.phone = contact_dict.get('Phone Number')
    temp_block.save()
    sleep(180)
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
        temporary_block_contact.delay(contact_dict)
        progress_recorder.set_progress(counter, progress_length,
                                       'Thank you for uploading your contacts, the upload is underway')
