from django.shortcuts import render
from django.views import View
from .models import Contact
import pandas as pd


class Home(View):

    def get(self, request):
        context = {'one': 'one'}
        return render(request, 'uploader/home.html', context)

    def post(self, request):
        contacts_file = pd.read_excel('files/test_file.xlsx', dtype=str)
        for index, cont in contacts_file.iterrows():
            cont = cont.to_dict()
            # This check is for NaN(when phone number is missing)
            if cont.get('Phone Number') == cont.get('Phone Number'):
                contact = Contact()
                contact.name = cont.get('Name')
                contact.phone = cont.get('Phone Number')
                contact.email = cont.get('Email Address')
                contact.save()

        context = {
            'contacts': 'done',
        }

        return render(request, 'uploader/home.html', context)
