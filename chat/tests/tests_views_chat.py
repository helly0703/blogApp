import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from Account.models import Account




@pytest.mark.django_db
@pytest.fixture
def create_new_user():
    user1 = User.objects.create_user(username='Helly', email='helly@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user1.id).update(name='Helly Soni', birthday='2010-02-07', gender='FEMALE',
                                                    privacy_mode='PRIVATE', allow_notification='True')
    user2 = User.objects.create_user(username='testuser2', email='test@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user2.id).update(name='testuser2', birthday='2004-06-07', gender='MALE',
                                                    privacy_mode='PUBLIC', allow_notification='False')
    user3 = User.objects.create_user(username='testuser3', email='test1@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user3.id).update(name='testuser3', birthday='2002-01-09', gender='FEMALE',
                                                    privacy_mode='PRIVATE', allow_notification='True')
    user4 = User.objects.create_user(username='testuser4', email='test3@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user4.id).update(name='testuser4', birthday='2010-02-07', gender='FEMALE',
                                                    privacy_mode='PUBLIC', allow_notification='False')
    return user1, user2, user3, user4

@pytest.mark.django_db
@pytest.fixture
def login_user1(create_new_user, client):
    data = {
        'username': 'Helly',
        'password': 'abcd@123'
    }
    url = reverse('login')
    response = client.post(url, data)
    # print(response.url)
    assert response.status_code == 302
    return response

@pytest.mark.django_db
def test_chat_home_view(create_new_user,login_user1, client):
    url = reverse('start-chat')
    response = client.get(url)
    # print(response.url)
    assert response.status_code == 200