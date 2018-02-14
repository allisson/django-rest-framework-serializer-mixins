from __future__ import absolute_import

import pytest

from testapp.models import Post
from testapp.serializers import DynamicPostSerializer


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user('user', 'user@email.com', '123456')


@pytest.fixture
def post(user):
    return Post.objects.create(
        user=user,
        title='Post Title',
        body='Post Body'
    )


@pytest.fixture
def dynamic_post_serializer_class():
    return DynamicPostSerializer
