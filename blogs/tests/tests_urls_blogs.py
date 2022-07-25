import pytest
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from Account.models import Account
from blogs.models import Category
# from blogs.views import SearchBlogView, HomeView, PostCreateView


@pytest.mark.django_db
@pytest.fixture
def register_user2(create_new_user, client):
    data = {
        'username': 'Helly',
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
def create_categories():
    new_category = Category.object.create(name='new_category')

# @pytest.mark.django_db
# def test_search_post_url(register_user2, login_user2,create_categories):
#     url = reverse('blogs')
#     print(url)
#     # assert resolve(url).func.view_class == PostCreateView
