import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from Account.models import Account
from blogs.models import Category, Post, Comment, SavePost


@pytest.mark.django_db
@pytest.fixture
def create_new_user():
    user1 = User.objects.create_user(username='Helly', email='helly@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user1.id).update(name='Helly Soni', birthday='2010-02-07', gender='FEMALE',
                                                    privacy_mode='PUBLIC', allow_notification='True')
    user2 = User.objects.create_user(username='testuser2', email='test@gmail.com', password='abcd@123')
    Account.objects.filter(user_id=user2.id).update(name='testuser2', birthday='2004-06-07', gender='MALE',
                                                    privacy_mode='PUBLIC', allow_notification='False')
    return user1, user2


@pytest.mark.django_db
@pytest.fixture
def login_user1(create_new_user, client):
    data = {
        'username': 'Helly',
        'password': 'abcd@123'
    }
    url = reverse('login')
    response = client.post(url, data)
    logged_in_user = User.objects.get(username='Helly')
    return logged_in_user


# login user2 fixture
@pytest.mark.django_db
@pytest.fixture
def login_user2(create_new_user, client):
    data = {
        'username': 'testuser2',
        'password': 'abcd@123'
    }
    url = reverse('login')
    response = client.post(url, data)
    logged_in_user = User.objects.get(username='testuser2')
    return logged_in_user

@pytest.mark.django_db
@pytest.fixture
def create_category():
    new_category = Category.objects.create(name="Education")
    new_category1 = Category.objects.create(name="Sports")
    new_category2 = Category.objects.create(name="Nature")
    new_category3 = Category.objects.create(name="Food")


@pytest.mark.django_db
@pytest.fixture
def create_blogs(create_new_user):
    new_user1 = User.objects.get(username="Helly")
    new_user2 = User.objects.get(username="testuser2")
    new_post1 = Post.objects.create(title="FirstPost", content="This id my first blog dbnshbdsah.", author=new_user1)
    new_post2 = Post.objects.create(title="SecondPost", content="This id my first blog dbnshbdsah.",
                                    author=new_user1,category="Sports")
    new_post3 = Post.objects.create(title="ThirdPost", content="This id my first blog dbnshbdsah.", author=new_user2)
    new_post4 = Post.objects.create(title="FourthPost", content="This id my first blog dbnshbdsah.",
                                    author=new_user2,category="Food")

@pytest.mark.django_db
@pytest.fixture
def save_post(create_new_user, create_blogs):
    user1 = User.objects.get(username='Helly')
    user2 = User.objects.get(username='testuser2')
    user2_id = user2.id
    new_account2 = Account.objects.get(user_id=user2_id)

    get_post = Post.objects.get(title="FirstPost")
    get_post.saved.add(new_account2)
    save_post = SavePost.objects.create(user=new_account2,post=get_post,value='Save')

@pytest.mark.django_db
@pytest.fixture
def unsave_post(create_new_user, create_blogs):
    user1 = User.objects.get(username='Helly')
    user2 = User.objects.get(username='testuser2')
    user2_id = user2.id
    new_account2 = Account.objects.get(user_id=user2_id)

    get_post = Post.objects.get(title="FirstPost")
    save_post = SavePost.objects.create(user=new_account2,post=get_post,value='Unsave')


@pytest.mark.django_db
class TestBlogHomeView:
    def test_home_view(self,create_new_user,login_user1,create_category,create_blogs,client):
        url = reverse('blogs')
        response = client.get(url)
        print(response)
        assert response.status_code == 200

    def test_home_view1(self,create_new_user,login_user1,create_category,client):
        url = reverse('blogs')
        response = client.get(url)
        print(response)
        assert response.status_code == 200

    def test_post_create_view(self,create_new_user,login_user1,create_category,client):
        data= {
                'title':'New Blog',
                'content':'It is the new blog',
                'category':'Education'
        }
        url = reverse('post-create')
        response = client.post(url,data)
        print(response)
        assert response.status_code == 302
        assert response.url == '/home/blogs/'

    def test_post_update_view1(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        data= {
                'title':'FirstPost Updated',
                'content':'It is the new blog updated',
                'category':'Education'
        }
        url = reverse('post-update',kwargs={'pk':new_post1.id})
        response = client.post(url,data)
        new_post2 = Post.objects.get(title="FirstPost Updated")
        print(new_post2.title)
        print(new_post2.content)
        print(response)
        assert response.status_code == 302
        assert response.url == '/home/blogs/'

    @pytest.mark.xfail
    def test_post_update_view2(self,create_new_user,login_user2,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        data= {
                'title':'FirstPost Updated',
                'content':'It is the new blog updated',
                'category':'Education'
        }
        url = reverse('post-update',kwargs={'pk':new_post1.id})
        response = client.post(url,data)
        new_post2 = Post.objects.get(title="FirstPost Updated")
        print(new_post2.title)
        print(new_post2.content)
        print(response)
        assert response.status_code == 302
        assert response.url == '/home/blogs/'

    def test_post_delete_view1(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('post-delete',kwargs={'pk':new_post1.id})
        response = client.get(url)
        try:
            new_post2 = Post.objects.get(title="FirstPost")
            # print(new_post2.title)
            print(new_post2.content)
        except Exception as e:
            print(f'Error {e}')
        print(response)
        assert response.status_code == 200

    def test_post_like_view(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('post-like', kwargs={'pk': new_post1.id})
        response = client.post(url,data={'post_id':new_post1.id})
        print(response)
        assert response.status_code == 200

    def test_post_like_view1(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('post-like', kwargs={'pk': new_post1.id})
        response = client.post(url,data={'post_id':new_post1.id})
        print(response)
        assert response.status_code == 200
        response = client.post(url, data={'post_id': new_post1.id})
        print(response)
        assert response.status_code == 200

    def test_post_comment_view(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('post-comment', kwargs={'pk': new_post1.id})
        response = client.post(url,data={'post_id':new_post1.id,'comment': "This is my comment"})
        print(response)
        assert response.status_code == 200

    def test_post_save_view(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('save-post')
        response = client.post(url,data={'post_id':new_post1.id})
        print(response)
        assert response.status_code == 200

    def test_post_save_view1(self,create_new_user,login_user1,create_blogs,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('save-post')
        response = client.post(url,data={'post_id':new_post1.id})
        print(response)
        response = client.post(url, data={'post_id': new_post1.id})
        print(response)
        assert response.status_code == 200

    def test_post_save_view2(self,create_new_user,login_user2,create_blogs,save_post,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('save-post')
        response = client.post(url, data={'post_id': new_post1.id})
        print(response)
        assert response.status_code == 200

    def test_post_save_list_view2(self, create_new_user, login_user2, create_blogs, save_post,client):
        new_post1 = Post.objects.get(title="FirstPost")
        url = reverse('post-saved')
        response = client.get(url)
        print(response)
        assert response.status_code == 200

    def test_post_filter_view(self, create_new_user, login_user2, create_blogs,create_category,client):
        url = reverse('category-list')
        response = client.get(url, data={'category-id': "Sports"})
        print(response)
        assert response.status_code == 200

    def test_post_filter_view1(self, create_new_user, login_user2, create_blogs,create_category,client):
        url = reverse('category-list')
        response = client.get(url, data={'category-id': ""})
        print(response)
        assert response.status_code == 200

    def test_category_list_view(self, create_new_user, login_user2, create_blogs,create_category,client):
        url = reverse('filter-blog')
        response = client.get(url)
        print(response)
        assert response.status_code == 200

    def test_search_blog_view(self,create_new_user, login_user2, create_blogs,create_category,client):
        url = reverse('search_post')
        response = client.get(url,data={'search_field':'First'})
        print(response)
        assert response.status_code == 200





