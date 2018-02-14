def test_dynamic_fields_mixin_fields(post, dynamic_post_serializer_class):
    serializer = dynamic_post_serializer_class(post)
    data = serializer.data
    assert 'id' in data
    assert 'user' in data
    assert 'title' in data
    assert 'body' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    serializer = dynamic_post_serializer_class(post, fields=('title', 'body'))
    data = serializer.data
    assert 'id' not in data
    assert 'user' not in data
    assert 'title' in data
    assert 'body' in data
    assert 'created_at' not in data
    assert 'updated_at' not in data


def test_dynamic_fields_mixin_read_only_fields(post, dynamic_post_serializer_class):
    serializer = dynamic_post_serializer_class(post, data={'title': 'Title', 'body': 'Body'})
    assert serializer.is_valid() is True
    serializer.save()
    data = serializer.data
    assert data['title'] == 'Title'
    assert data['body'] == 'Body'

    serializer = dynamic_post_serializer_class(post, data={'title': 'New Title', 'body': 'New Body'}, read_only_fields=('title', 'body'))
    assert serializer.is_valid() is True
    serializer.save()
    data = serializer.data
    assert data['title'] == 'Title'
    assert data['body'] == 'Body'
