from django.shortcuts import render
from django.views import View
from .models import Contact, File
import pandas as pd


class Home(View):

    def get(self, request):
        context = {'one': 'one'}
        return render(request, 'uploader/home.html', context)

    def post(self, request):
        context = {}
        excel_file = request.FILES.get('excel_file')

        if excel_file:
            if excel_file.size > 10485760:
                context['error'] = 'File size should be less than 10mb'
            elif not excel_file.name.endswith('xlsx'):
                context['error'] = 'File format should be xlsx'
            else:
                file = File()
                file.name = excel_file.name
                file.file = excel_file
                file.save()

                contacts_file = pd.read_excel(file.file, dtype=str)
                for index, cont in contacts_file.iterrows():
                    cont = cont.to_dict()
                    # This check is for NaN(when phone number is missing)
                    if cont.get('Phone Number') == cont.get('Phone Number'):
                        contact = Contact()
                        contact.name = cont.get('Name')
                        contact.phone = cont.get('Phone Number')
                        contact.email = cont.get('Email Address')
                        contact.save()

                context['status'] = 'Success'
        return render(request, 'uploader/home.html', context)
