# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category (models.Model):
	name = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							db_index=True,
							unique=True)
	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category,
								related_name='Products')
	name = models.CharField(max_length=200,
							db_index=True)
	slug = models.SlugField(max_length=200,
							db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d',
							blank=True)
	description = models.TextField(max_digits=10)