django-rest-framework-serializer-mixins
=======================================

.. image:: https://travis-ci.org/allisson/django-rest-framework-serializer-mixins.svg?branch=master
    :target: https://travis-ci.org/allisson/django-rest-framework-serializer-mixins

.. image:: https://codecov.io/gh/allisson/django-rest-framework-serializer-mixins/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/allisson/django-rest-framework-serializer-mixins

.. image:: https://img.shields.io/pypi/v/djangorestframework-serializer-mixins.svg
        :target: https://pypi.python.org/pypi/djangorestframework-serializer-mixins

.. image:: https://img.shields.io/github/license/allisson/django-rest-framework-serializer-mixins.svg
        :target: https://pypi.python.org/pypi/djangorestframework-serializer-mixins

.. image:: https://img.shields.io/pypi/pyversions/djangorestframework-serializer-mixins.svg
        :target: https://pypi.python.org/pypi/djangorestframework-serializer-mixins


Mixins for Django Rest Framework Serializer

How to install
--------------

.. code:: shell

    pip install djangorestframework-serializer-mixins

How to use DynamicFieldsMixin
-----------------------------

Assume you have a Post model:

.. code:: python

    # testapp/models.py
    from django.conf import settings
    from django.db import models


    class Post(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
        title = models.CharField(max_length=128)
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title

        class Meta:
            ordering = ['-created_at']


Write DynamicPostSerializer with DynamicFieldsMixin:

.. code:: python

    # testapp/serializers.py
    from rest_framework import serializers

    from rest_framework_serializer_mixins import DynamicFieldsMixin

    from .models import Post


    class DynamicPostSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = (
                'body',
                'created_at',
                'id',
                'title',
                'updated_at',
                'user',
            )
            read_only_fields = (
                'id',
                'user',
            )

Now, you can define fields and read_only_field like this:

.. code:: python

    >>> from django.contrib.auth.models import User
    >>> from testapp.models import Post
    >>> from testapp.serializers import DynamicPostSerializer
    >>> user = User.objects.create_user('user', 'user@email.com', '123456')
    >>> post = Post.objects.create(user=user, title='My Title', body='My Body')
    >>> serializer = DynamicPostSerializer(post) # return fields and read_only_fields from Meta
    >>> serializer.data
    {'body': 'My Body', 'created_at': '2018-02-14T14:15:29.772209Z', 'id': 1, 'title': 'My Title', 'updated_at': '2018-02-14T14:15:29.772312Z', 'user': 1}
    >>> serializer = DynamicPostSerializer(post, fields=('title', 'body')) # return only title and body fields
    >>> serializer.data
    {'body': 'My Body', 'title': 'My Title'}
    >>> serializer = DynamicPostSerializer(post, read_only_fields=('title', 'body'), data={'title': 'New Title', 'body': 'New Body'}) # set title and body as read_only_fields
    >>> serializer.is_valid()
    True
    >>> serializer.save()
    <Post: My Title>
    >>> serializer.data
    {'body': 'My Body', 'created_at': '2018-02-14T14:15:29.772209Z', 'id': 1, 'title': 'My Title', 'updated_at': '2018-02-14T14:19:14.838001Z', 'user': 1} # title and body don't change
