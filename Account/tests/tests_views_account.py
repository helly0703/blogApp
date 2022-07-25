from unittest import TestCase

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from Account.models import Account, Relationship


# Creating users
from blogs.models import Category, Post


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


# Registering user2 fixture
@pytest.mark.django_db
@pytest.fixture
def register_user2(create_new_user, client):
    data = {
        'username': 'Priya',
        'email': 'piyu@gmail.com',
        'password1': 'abcd@123',
        'password2': 'abcd@123',
        'birthdate': '2015-12-01'
    }
    path = reverse('register')
    response = client.post(path, data)
    new_user = User.objects.get(username='Priya')
    new_user_account = Account.objects.get(user=new_user)
    print(f'new_user   :   {new_user.username}  {new_user.email}')
    print(f'new_user_account   :   {new_user_account.name} {new_user_account.birthday}')
    # print(response.url)
    assert response.url == '/accounts/login/'


# login user1 fixture
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

# test login view
@pytest.mark.django_db
class TestUserLogin:
    # Correct username, password login check
    def test_login_user1(self, create_new_user, client):
        data = {
            'username': 'Helly',
            'password': 'abcd@123'
        }
        url = reverse('login')
        response = client.post(url, data)
        print(response.url)
        assert response.status_code == 302

    # Incorrect username, password login check
    @pytest.mark.xfail
    def test_login_user2(self, create_new_user, client):
        data = {
            'username': 'Shivani',
            'password': 'abcd@123'
        }
        url = reverse('login')
        response = client.post(url, data)
        print(response)
        assert response.status_code == 302


# test registration view
@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user1(self, create_new_user, client):
        data = {
            'username': 'Shivani',
            'email': 'test@gmail.com',
            'password1': 'abcd@123',
            'password2': 'abcd@123',
            'birthdate': '2015-12-01'
        }
        path = reverse('register')
        response = client.post(path, data)
        assert response.url == '/accounts/login/'

    @pytest.mark.xfail
    def test_register_user2(self, create_new_user, client):
        data = {
            'username': 'Helly',
            'email': 'test@gmail.com',
            'password1': 'abcd@123',
            'password2': 'abcd@123',
            'birthdate': '2015-12-01'
        }
        url = reverse('register')
        response = client.post(url, data)

        print(response)
        assert response.url == '/accounts/login/'


# check user object(Correct Test case)
@pytest.mark.django_db
def test_check_user1(create_new_user):
    try:
        check_user = User.objects.get(username='Helly')
    except Exception as e:
        check_user = False
    assert check_user


# check user object(Incorrect TestCase)
@pytest.mark.django_db
@pytest.mark.xfail
def test_check_user2(create_new_user):
    try:
        check_user = User.objects.get(username='Shivani')
    except Exception as e:
        check_user = False
    assert check_user


# check if homepage available
@pytest.mark.django_db
class TestHomePageDisplay:
    # (Correct test case )
    def test_display_homepage(self, create_new_user, login_user1, client):
        path = reverse('home')
        response = client.get(path)
        print(response)
        assert response.url == '/home/blogs/'

    # (Incorrect test case )
    @pytest.mark.xfail
    def test_display_homepage1(self, create_new_user, client):
        path = reverse('home')
        response = client.get(path)
        print(response)
        assert response.url == '/home/blogs/'


# check if profile view available
@pytest.mark.django_db
class TestProfileView:
    # (Correct test case )
    def test_display_homepage(self, create_new_user, login_user1, client):
        path = reverse('view_profile')
        response = client.get(path)
        print(response)
        print(response.request)
        assert response.status_code == 200

    # (Incorrect test case )
    @pytest.mark.xfail
    def test_display_homepage1(self, create_new_user, client):
        path = reverse('view_profile')
        response = client.get(path)
        print(response)
        assert response.status_code == 200


# Update Account view get post forms test
@pytest.mark.django_db
class TestUpdateAccountDetailsView:
    # Get form filled with existing data(Correct test case)
    def test_update_get_account1(self, register_user2, login_user2, client):
        path = reverse('profile')
        response = client.get(path)
        print(response)
        print(f'----------Get account details----------------')
        assert response.status_code == 200
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            email = login_user2.email
            print(email)
            username = login_user2.username
            print(username)
            name = get_account.name
            print(name)
            birth_date = get_account.birthday
            print(birth_date)
            gender = get_account.gender
            print(f'{get_account.name},{get_account.birthday},{get_account.gender}')
        except Exception as e:
            print(f'Error {e}')

    # Submit form (Correct test case)
    def test_update_post_account1(self, register_user2, login_user2, client):
        path = reverse('profile')
        data = {
            'email': 'priya@gmail.com',
            'username': 'priya',
            'name': 'Priya Patel',
            'gender': 'MALE',
            'birthday': '2012-08-08',
            'description': 'POPPI',
            'image': ''
        }
        response = client.post(path, data)
        print(response)
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            print(f'Account-Name :  {get_account.name},')
            print(f'\nBirthday:    {get_account.birthday},')
            print(f'\nGender: {get_account.gender}\n')
            print(f'Description: {get_account.description}')
            print(f'\nEmail:    {login_user2.email}')
            print(f'\nusername:    {login_user2.username}')
        except Exception as e:
            print(f'Error {e}')
        assert response.status_code == 302

    # Submit form(Incorrect test case)
    @pytest.mark.xfail
    def test_update_post_account2(self, register_user2, login_user2, client):
        path = reverse('profile')
        data = {
            'email': '',
            'username': 'priya',
            'name': 'Priya Patel',
            'gender': 'FEMALE',
            'birthday': '2012-08-08',
            'description': 'POPPI',
            'image': ''
        }
        response = client.post(path, data)
        print(response)
        assert response.status_code == 302
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            print(f'Account-Name :  {get_account.name},')
            print(f'Birthday:    {get_account.birthday},')
            print(f'Gender: {get_account.gender}')
            print(f'Description: {get_account.description}')
            print(f'Email:    {login_user2.email}')
            print(f'username:    {login_user2.username}')
        except Exception as e:
            print(f'Error {e}')


@pytest.mark.django_db
class TestUpdateAccountSettingsView:
    # Get account settings form filled (Correct test case)
    def test_update_get_account_settings1(self, register_user2, login_user2, client):
        path = reverse('settings')
        response = client.get(path)
        print(response)
        print(f'----------Get account details----------------')
        assert response.status_code == 200
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            email = login_user2.email
            print(email)
            username = login_user2.username
            print(username)
            privacy_mode = get_account.privacy_mode
            print(f'privacy_mode:  {privacy_mode}')
            allow_notification = get_account.allow_notification
            print(f'allow_notification:  {allow_notification}')
        except Exception as e:
            print(f'Error {e}')

    # Submit form (Correct test case)
    def test_update_post_account_settings1(self, register_user2, login_user2, client):
        path = reverse('settings')
        data = {
            'privacy_mode': 'PUBLIC',
            'allow_notification': 'False',
        }
        response = client.post(path, data)
        print(response)
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            print(f'Allow Notifications :  {get_account.allow_notification},')
            print(f'Privacy Mode:    {get_account.privacy_mode},')
        except Exception as e:
            print(f'Error {e}')
        assert response.status_code == 302

    # Submit form(Incorrect test case)
    @pytest.mark.xfail
    def test_update_post_account_settings2(self, register_user2, login_user2, client):
        path = reverse('settings')
        data = {
            'privacy_mode': '',
            'allow_notification': 'False',
        }
        response = client.post(path, data)
        print(response)
        try:
            get_account = Account.objects.get(user_id=login_user2.id)
            print(f'Allow Notifications :  {get_account.allow_notification}')
            print(f'Privacy Mode:    {get_account.privacy_mode}')
        except Exception as e:
            print(f'Error {e}')
        assert response.status_code == 302


def test_logout():
    pass


@pytest.mark.django_db
def login_any_user(client,data):
    url = reverse('login')
    response = client.post(url, data)
    print(response.url)
    print("Checking test send friend kjdsfjdsnfkdsfnkdsnfdksnfkdsnknkjdsfnsnkj===================")
    assert response.status_code == 302
    return client.post(url, data)

# @pytest.mark.django_db
# def add_friends()


@pytest.mark.django_db
def test_send_friend_request1(create_new_user,login_user2,client):
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
@pytest.mark.xfail
def test_send_friend_request1(create_new_user,login_user2,client):
    url = reverse('send_invite')
    test_user = User.objects.get(username="testuser3")
    test_friend = Account.objects.get(user_id=test_user)
    response = client.post(url,data={'profile_pk':test_friend.id})
    print(response)
    request_sent = Relationship.objects.last()
    # request_received = Relationship.objects.get(receiver='testuser2')
    print(test_friend.privacy_mode)
    print("Checking test send friend kjdsfjdsnfkdsfnkdsnfdksnfkdsnknkjdsfnsnkj===================")
    assert request_sent.sender.name == login_user2.account.name
    assert request_sent.receiver.name == "testuser3"
    assert request_sent.status == "accepted"

@pytest.mark.django_db
def test_friend_detail_view(create_new_user,login_user2,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('friend_detail',kwargs={'pk': test_user_account.id})
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.fixture
def login_user_3(create_new_user, client):
    data = {
    'username': 'testuser3',
    'password': 'abcd@123'
    }
    url = reverse('login')
    response = client.post(url, data)
    # print(response.url)
    assert response.status_code == 302

@pytest.mark.django_db
@pytest.fixture
def send_request(create_new_user,login_user_3, client):
    user = User.objects.get(username="Helly")
    account = Account.objects.get(user_id=user.id)
    url2=reverse('send_invite')
    response2 = client.post(url2,data={'profile_pk':account.id})
    assert response2.status_code == 200

@pytest.mark.django_db
@pytest.fixture
def send_request_1(create_new_user,client):
    user1 = User.objects.get(username="Helly")
    account1 = Account.objects.get(user_id=user1.id)
    user2 = User.objects.get(username="testuser3")
    account2 = Account.objects.get(user_id=user2.id)
    new_request = Relationship.objects.create(sender=account2,receiver=account1,status='send')




@pytest.mark.django_db
def test_invites_received_view(create_new_user,login_user2,send_request,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('my_invites')
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_accept_invite_view(create_new_user,login_user2,send_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('accept_request')
    response = client.post(url,data={'profile_pk':test_user_account.id})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_reject_invite_view(create_new_user,login_user2,send_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('remove_request')
    response = client.post(url,data={'profile_pk':test_user_account.id})
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.fixture
def accepted_request_1(create_new_user,client):
    user1 = User.objects.get(username="Helly")
    account1 = Account.objects.get(user_id=user1.id)
    user2 = User.objects.get(username="testuser3")
    account2 = Account.objects.get(user_id=user2.id)
    new_request = Relationship.objects.create(sender=account2,receiver=account1,status='accepted')

@pytest.mark.django_db
def test_block_user_create_view(create_new_user,login_user2,accepted_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('block_profile')
    response = client.post(url,data={'profile_pk':test_user.id})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_search_profile_view(create_new_user,login_user2,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('search_profile')
    response = client.get(url,data={'search_field':"test"})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_remove_friend_view(create_new_user,login_user2,accepted_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('remove_friend')
    response = client.post(url,data={'profile_pk':test_user_account.id})
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.fixture
def create_blog(create_new_user,login_user2,client):
    user1 = User.objects.get(username="Helly")
    account1 = Account.objects.get(user_id=user1.id)
    new_category = Category.objects.create(name="Education")
    new_blog = Post.objects.create(title="FirstPost", content="This id my first blog dbnshbdsah.",author=user1)

@pytest.mark.django_db
def test_my_blogs_view(create_new_user,login_user2,create_blog,client):
    url = reverse('my_blogs')
    response = client.get(url)
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.fixture
def block_user(create_new_user,login_user2,accepted_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('block_profile')
    response = client.post(url,data={'profile_pk':test_user.id})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_unblock_user_view(create_new_user,login_user2,accepted_request_1,block_user,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('unblock_friend')
    response = client.post(url, data={'profile_pk': test_user.id})
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.fixture
def block_user_1(create_new_user,login_user2,accepted_request_1,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    test_user_account.privacy_mode="PUBLIC"
    test_user_account.save()
    url = reverse('block_profile')
    response = client.post(url,data={'profile_pk':test_user.id})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_unblock_user_view_1(create_new_user,login_user2,accepted_request_1,block_user,client):
    test_user = User.objects.get(username="testuser3")
    test_user_account = Account.objects.get(user_id=test_user.id)
    url = reverse('unblock_friend')
    response = client.post(url, data={'profile_pk': test_user.id})
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_invites_list_view(create_new_user,login_user2,send_request_1,client):
    url = reverse('invite_profiles')
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_all_profiles_list_view(create_new_user,login_user2,client):
    url = reverse('all_profiles')
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.fixture
def make_user_public(create_new_user):
    test_user = User.objects.get(username="testuser3")
    test_friend = Account.objects.get(user_id=test_user)
    test_friend.privacy_mode="PUBLIC"
    test_friend.save()

@pytest.mark.django_db
def test_send_friend_request2(create_new_user,login_user2,make_user_public,block_user,client):
    url = reverse('send_invite')
    test_user = User.objects.get(username="testuser3")
    test_friend = Account.objects.get(user_id=test_user)
    response = client.post(url,data={'profile_pk':test_friend.id})
    print(response)
    request_sent = Relationship.objects.last()
    # request_received = Relationship.objects.get(receiver='testuser2')
    print(test_friend.privacy_mode)
    print("Checking test send friend kjdsfjdsnfkdsfnkdsnfdksnfkdsnknkjdsfnsnkj===================")
    assert request_sent.sender.name == login_user2.account.name
    assert request_sent.receiver.name == "testuser3"
    assert request_sent.status == "accepted"