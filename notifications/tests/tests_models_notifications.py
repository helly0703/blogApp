import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from Account.models import Account, Relationship
from notifications.models import Notifications


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

# login user2 fixture
@pytest.mark.django_db
@pytest.fixture
def login_user2(create_new_user, client):
    data = {
        'username': 'Helly',
        'password': 'abcd@123'
    }
    url = reverse('login')
    response = client.post(url, data)
    # print(response.url)
    assert response.status_code == 302
    logged_in_user = User.objects.get(username='Helly')
    return logged_in_user


@pytest.mark.django_db
@pytest.fixture
def send_friend_request1(create_new_user,login_user2,client):
    url = reverse('send_invite')
    test_user = User.objects.get(username="testuser2")
    test_friend = Account.objects.get(user_id=test_user)
    response = client.post(url,data={'profile_pk':test_friend.id})
    print(response)
    request_sent = Relationship.objects.last()
    # request_received = Relationship.objects.get(receiver='testuser2')
    print(test_friend.privacy_mode)
    print("Checking test send friend kjdsfjdsnfkdsfnkdsnfdksnfkdsnknkjdsfnsnkj===================")
    assert request_sent.sender.name == login_user2.account.name
    assert request_sent.receiver.name == "testuser2"
    assert request_sent.status == "accepted"

@pytest.mark.django_db
def test_str_post(create_new_user, login_user2,send_friend_request1,client):
    test_user = User.objects.get(username="Helly")
    test_friend = Account.objects.get(user_id=test_user)
    new_notification = Notifications.objects.get(to_user=test_friend)
    assert str(new_notification) == test_user.username

@pytest.mark.django_db
@pytest.fixture
def allow_notification(create_new_user):
    test_user = User.objects.get(username="Helly")
    test_friend = Account.objects.get(user_id=test_user)
    test_friend.allow_notification=True
    test_friend.save()

@pytest.mark.django_db
def test_notify_user_1(create_new_user, login_user2,send_friend_request1,allow_notification,client):
    test_user = User.objects.get(username="Helly")
    test_friend = Account.objects.get(user_id=test_user)
    new_notification = Notifications.objects.get(to_user=test_friend)
    print(new_notification.notify_user())
    assert new_notification.notify_user() == "You and testuser2 are now friends"

@pytest.mark.django_db
@pytest.fixture
def not_allow_notification(create_new_user):
    test_user = User.objects.get(username="Helly")
    test_friend = Account.objects.get(user_id=test_user)
    test_friend.allow_notification=False
    test_friend.save()

@pytest.mark.django_db
def test_notify_user_2(create_new_user, login_user2,send_friend_request1,not_allow_notification,client):
    test_user = User.objects.get(username="Helly")
    test_friend = Account.objects.get(user_id=test_user)
    new_notification = Notifications.objects.get(to_user=test_friend)
    print(new_notification.notify_user())
    assert new_notification.notify_user() == "You and testuser2 are now friends"