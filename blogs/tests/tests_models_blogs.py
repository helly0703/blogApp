import pytest
from django.urls import resolve

from Account.models import Account, Relationship
from blogs.models import Post, Comment, Category, Like, SavePost
from django.contrib.auth.models import User

# from blogs.views import PostDetailView


@pytest.mark.django_db
@pytest.fixture
def create_user1():
    print("YEs")
    new_user1 = User.objects.create(username="testuser1", email="testuser@gmail.com", password="abcd@123")
    new_user1_id = new_user1.id
    new_account1 = Account.objects.get(user_id=new_user1_id)
    new_account1.name = "test2"
    new_account1.birthday = "2001-05-09"
    new_account1.gender = "FEMALE"
    new_account1.privacy_mode = "PUBLIC"
    new_account1.save()
    return new_account1


@pytest.mark.django_db
@pytest.fixture
def create_user2():
    new_user2 = User.objects.create(username="testuser2", email="testuser@gmail.com", password="abcd@123")
    new_user2_id = new_user2.id
    new_account2 = Account.objects.get(user_id=new_user2_id)
    new_account2.name = "test3"
    new_account2.birthday = "2001-05-09"
    new_account2.gender = "FEMALE"
    new_account2.privacy_mode = "PRIVATE"
    new_account2.save()

@pytest.mark.django_db
@pytest.fixture
def create_category():
    new_category = Category.objects.create(name="Education")


@pytest.mark.django_db
@pytest.fixture
def create_blog1(create_user1):
    new_user1 = User.objects.get(username="testuser1")
    new_post1 = Post.objects.create(title="FirstPost", content="This id my first blog dbnshbdsah.", author=new_user1)


@pytest.mark.django_db
class TestPostModel:
    def test_post_model_create(self, create_user1, create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_post = Post.objects.create(title="FirstPost", content="This id my first blog dbnshbdsah.", author=new_user1)
        assert new_post.title == "FirstPost"

    def test_num_of_likes(self, create_user1, create_user2):
        new_user1 = User.objects.get(username="testuser1")

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        new_post = Post.objects.create(title="FirstPost", content="This id my first blog dbnshbdsah.", author=new_user1)
        new_post.liked.add(new_account2)
        new_post.save()
        post = Post.objects.get(title="FirstPost")
        assert post.num_of_likes() == 1



    def test_get_comments(self, create_user1, create_user2, create_blog1):
        new_user1 = User.objects.get(username="testuser1")
        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        get_post = Post.objects.get(title="FirstPost")
        post_comment = Comment.objects.create(user=new_account2,post=get_post,body="nice one")
        post_comment1 = Comment.objects.create(user=new_account2,post=get_post,body="second")
        post_comment2 = Comment.objects.create(user=new_account2,post=get_post,body="third")
        post_comment3 = Comment.objects.create(user=new_account2,post=get_post,body="good")
        post_comment4 = Comment.objects.create(user=new_account2,post=get_post,body="awesome")

        post = Post.objects.get(title="FirstPost")
        comments_list = post.get_comments()
        assert comments_list[0] == post_comment4
        assert comments_list[1] == post_comment3
        assert comments_list[2] == post_comment2
        assert comments_list[3] == post_comment1
        assert comments_list[4] == post_comment

    def test_num_of_comments(self, create_user1, create_user2, create_blog1):
        new_user1 = User.objects.get(username="testuser1")

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        get_post = Post.objects.get(title="FirstPost")
        post_comment = Comment.objects.create(user=new_account2,post=get_post,body="nice one")
        post = Post.objects.get(title="FirstPost")
        comments_count = post.num_of_comments()
        assert comments_count == 1

    def test_get_absolute_url(self,create_user1,create_blog1,create_category):
        new_post1 = Post.objects.get(title="FirstPost")
        new_category = Category.objects.get(name="Education")
        assert new_post1.get_absolute_url() == '/home/blogs/blogpost/6/'

    def test_get_absolute_url_categories(self, create_user1, create_blog1, create_category):
        new_post1 = Post.objects.get(title="FirstPost")
        new_category = Category.objects.get(name="Education")
        # assert new_post1.get_absolute_url() == '/home/blogs/blogpost/5/'

        print(new_category.get_absolute_url())
        assert new_category.get_absolute_url() == '/home/blogs/'

    def test_str_post(self, create_user1, create_blog1):
        new_post1 = Post.objects.get(title="FirstPost")
        assert str(new_post1) == 'FirstPost'

    def test_str_category(self, create_user1, create_category):
        new_category = Category.objects.get(name="Education")

        assert str(new_category) == 'Education'

    def test_str_comment(self, create_user1, create_user2, create_blog1):
        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        get_post = Post.objects.get(title="FirstPost")
        post_comment = Comment.objects.create(user=new_account2,post=get_post,body="nice one")

        assert str(post_comment) == str(post_comment.id)

    def test_str_like_post(self,create_user1, create_user2, create_blog1):
        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        get_post = Post.objects.get(title="FirstPost")
        new_like = Like.objects.create(user=new_account2,post=get_post,value='Like')
        assert str(new_like) == f'{new_account2}-{get_post}-Like'

    def test_str_save_post(self,create_user1, create_user2, create_blog1):
        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        get_post = Post.objects.get(title="FirstPost")
        save_post = SavePost.objects.create(user=new_account2,post=get_post,value='Save')
        assert str(save_post) == f'{new_account2}-{get_post}-Save'








