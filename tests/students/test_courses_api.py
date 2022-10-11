import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# тестирование получения всех курсов
@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=20)
    url = reverse('courses-list')

    # Act
    response = client.get(url)
    data = response.data

    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)

# тестирование получения первого курса
@pytest.mark.django_db
def test_get_first_course(client, courses_factory):
    # Arrange
    course = courses_factory()
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response = client.get(url)
    data = response.data

    # Assert
    assert response.status_code == 200
    assert data['id'] == course.id

# тестирование фильтрации по id
@pytest.mark.django_db
def test_get_courses_filter_id(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=20)
    filter_course = courses[0].id
    filter_courses = []
    for course in courses:
        if int(course.id) == filter_course:
            filter_courses.append(course)
    url = f'/api/v1/courses/?id={filter_course}'
    # Act
    response = client.get(url)
    data = response.data

    # Assert
    assert response.status_code == 200
    assert len(data) == len(filter_courses)

# тестирование фильтрации по имени
@pytest.mark.django_db
def test_get_courses_filter_name(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=20)
    filter_course = courses[0].name
    filter_courses = []
    for course in courses:
        if course.name == filter_course:
            filter_courses.append(course)
    url = f'/api/v1/courses/?name={filter_course}'
    # Act
    response = client.get(url)
    data = response.data

    # Assert
    assert response.status_code == 200
    assert len(data) == len(filter_courses)


#тест успешного создания курса
@pytest.mark.django_db
def test_get_courses_post(client):
    # Arrange
    data_to_post = {"name": "123"}
    url = f'/api/v1/courses/'
    # Act
    response = client.post(url, data = data_to_post)
    data = response.data

    # Assert
    assert response.status_code == 201
    assert data['name'] == data_to_post['name']


#тест успешного обновления курса
@pytest.mark.django_db
def test_get_courses_patch(client, courses_factory):
    # Arrange
    course = courses_factory()
    data_to_patch = {"name": "123"}
    url = f'/api/v1/courses/{course.id}/'
    # Act
    response = client.patch(url, data = data_to_patch)
    data = response.data

    # Assert
    assert response.status_code == 200
    assert data['name'] == data_to_patch['name']


#тест успешного обновления курса
@pytest.mark.django_db
def test_get_courses_delete(client, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=20)
    url = f'/api/v1/courses/{courses[0].id}/'
    get_url = reverse('courses-list')
    # Act
    response = client.delete(url)
    # после удаления получаем весь список
    get_response = client.get(get_url)
    data = get_response.data

    # Assert
    assert response.status_code == 204
    # проверяем, что список после удаления стал меньше на 1
    assert len(data) == len(courses) - 1