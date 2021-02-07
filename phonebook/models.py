from django.db import models


class Contact(models.Model):

	name = models.CharField(
		max_length=30,
		blank=True
	)

	surname = models.CharField(
		max_length=30,
		blank=True
	)

	phone = models.CharField(
		max_length=30,
		blank=True
	)

	def __str__(self):
		return f'Contact No.{self.id}'

