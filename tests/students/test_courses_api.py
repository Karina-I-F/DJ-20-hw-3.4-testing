import pytest
from django.urls import reverse

from students.models import Course


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course_factory(_quantity=2)
    course = Course.objects.first()
    url = reverse('courses-detail', args=(course.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_filter_check_course_id(client, course_factory):
    course_factory(_quantity=5)
    course = Course.objects.first()
    url = reverse('courses-list')+f'?id={course.id}'
    response = client.get(url)
    assert response.status_code == 200
    for item in response.data:
        assert item['id'] == course.id


@pytest.mark.django_db
def test_filter_check_course_name(client, course_factory):
    course_factory(_quantity=5)
    course = Course.objects.first()
    url = reverse('courses-list')+f'?name={course.name}'
    response = client.get(url)
    assert response.status_code == 200
    for item in response.data:
        assert item['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    data ={
        "name": "Tests course",
        "students": []
    }
    url = reverse('courses-list')
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_factory(_quantity=5)
    course = Course.objects.first()
    url = reverse('courses-detail', args=(course.id, ))
    data = {
        "name": "The best course",
        "students": []
    }
    response = client.patch(url, data)
    assert response.status_code == 200
    assert response.data['name'] == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=5)
    course = Course.objects.first()
    url = reverse('courses-detail', args=(course.id, ))
    response = client.delete(url)
    assert response.status_code == 204
    assert response.data is None
