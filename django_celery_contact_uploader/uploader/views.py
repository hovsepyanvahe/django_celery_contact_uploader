from django.shortcuts import render
from django.views import View
from .models import TemporaryBlockedContact, File
from django.db.models import Q
import pandas as pd
from .tasks import temporary_block_contact,unblock_contacts, process_contacts
from datetime import datetime, timedelta


class Home(View):

    def get(self, request):
        return render(request, 'uploader/home.html')

    def post(self, request):
        context = {}
        excel_file = request.FILES.get('excel_file')

        if excel_file:
            if excel_file.size > 10485760:
                context['error'] = 'File size should be less than 10mb'
            elif not excel_file.name.endswith('xlsx'):
                context['error'] = 'File format should be xlsx'
            else:
                list_of_valid_contacts = []
                contacts_file = pd.read_excel(excel_file, dtype=str)
                for index, cont in contacts_file.iterrows():
                    cont = cont.to_dict()

                    if self.is_contact_valid(cont) and not self.is_temporary_blocked(cont):
                        list_of_valid_contacts.append(cont)

                task = process_contacts.delay(list_of_valid_contacts)
                context['task_id'] = task.task_id
                temporary_block_contact.delay(list_of_valid_contacts)
                after_3_minutes = datetime.utcnow() + timedelta(minutes=3)
                unblock_contacts.apply_async([list_of_valid_contacts], eta=after_3_minutes)

                file = File()
                file.name = excel_file.name
                file.file = excel_file
                file.save()

        return render(request, 'uploader/home.html', context)

    def is_contact_valid(self, contact_dict):
        contact_name = contact_dict.get('Name')
        contact_email = contact_dict.get('Email Address')
        contact_phone = contact_dict.get('Phone Number')

        # This check is for NaN(when phone number is missing)
        if contact_phone != contact_phone:
            return False
        elif not contact_name and not contact_email:
            return False

        return True

    def is_temporary_blocked(self, contact_dict):
        contact_email = contact_dict.get('Email Address')
        contact_phone = contact_dict.get('Phone Number')
        contact = TemporaryBlockedContact.objects.filter(Q(email=contact_email) | Q(phone=contact_phone))

        if contact.exists():
            return True

        return False
