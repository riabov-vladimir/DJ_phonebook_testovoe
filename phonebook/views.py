from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from phonebook.serializers import *
from phonebook.models import *


class ContactDetail(APIView):

    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Изменить контакт с указанным id"""
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Удалить контакт по id"""
        try:
            contact = Contact.objects.get(id=pk)
            contact.delete()
            return Response(data=f'Contact No.{pk} deleted', status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            raise Http404


class ContactList(APIView):
    """Отобразить все контакты"""
    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Создать новый контакт"""
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            contact = Contact.objects.last()
            return Response(f'{contact} created', status=status.HTTP_201_CREATED)  # serializer.data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

