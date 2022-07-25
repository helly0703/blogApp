import pytest
from Account.models import Account, Relationship
from django.contrib.auth.models import User

@pytest.mark.django_db
@pytest.fixture
def create_user1():
    new_user1 = User.objects.create(username="testuser1", email="testuser@gmail.com", password="abcd@123")
    new_user1_id = new_user1.id
    new_account1 = Account.objects.get(user_id=new_user1_id)
    new_account1.name = "test2"
    new_account1.birthday = "2001-05-09"
    new_account1.gender = "FEMALE"
    new_account1.privacy_mode = "PUBLIC"
    new_account1.save()

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
class TestAccountModel:

    def test_account_model(self):
        new_user = User.objects.create(username="testuser", email="testuser@gmail.com", password="abcd@123")

        new_user1 = User.objects.create(username="testuser1", email="testuser@gmail.com", password="abcd@123")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)
        new_account1.name = "test2"
        new_account1.birthday = "2001-05-09"
        new_account1.gender = "FEMALE"
        new_account1.privacy_mode = "PUBLIC"
        new_account1.save()

        new_user2 = User.objects.create(username="testuser2", email="testuser@gmail.com", password="abcd@123")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)
        new_account2.name = "test3"
        new_account2.birthday = "2001-05-09"
        new_account2.gender = "FEMALE"
        new_account2.privacy_mode = "PRIVATE"
        new_account2.save()

        # assert new_user.username == "testuser"
        new_user_id = new_user.id
        new_account = Account.objects.get(user_id=new_user_id)
        new_account.name = "test"
        new_account.birthday = "2001-05-09"
        new_account.gender = "FEMALE"
        # new_account.friendslist = new_account.friendslist + [new_user2]
        new_account.save()

        # assert new_account.name == "test"
        # assert new_account.birthday=="2001-05-09"
        # assert new_account.gender == "FEMALE"

        public_users = new_account.get_user_public()
        print(public_users)

        assert [new_user1] == public_users
        assert public_users != [new_user2]
        assert len(public_users) == 1

    def test_get_friends(self):
        new_user1 = User.objects.create(username="testuser1", email="testuser@gmail.com", password="abcd@123")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)
        new_account1.name = "test2"
        new_account1.birthday = "2001-05-09"
        new_account1.gender = "FEMALE"
        new_account1.privacy_mode = "PUBLIC"
        new_account1.save()

        new_user2 = User.objects.create(username="testuser2", email="testuser@gmail.com", password="abcd@123")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)
        new_account2.name = "test3"
        new_account2.birthday = "2001-05-09"
        new_account2.gender = "FEMALE"
        new_account2.privacy_mode = "PRIVATE"
        new_account2.save()

        new_friends = Relationship.objects.create(sender=new_account1, receiver=new_account2,status='accepted')
        friends_list = new_account2.get_friends()
        print(friends_list)
        assert friends_list[0] == new_user1

    def test_get_friends_no(self, create_user1, create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        new_friends = Relationship.objects.create(sender=new_account1, receiver=new_account2, status='accepted')
        friends_count = new_account2.get_friends_no()
        assert friends_count == 1

    def test_get_blocklist(self, create_user1, create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        new_account2.blockedlist.add(new_user1)

        blocked_user = new_account2.get_blocklist()
        print(f'blocked user  {blocked_user}')
        assert blocked_user[0] == new_user1

    def test_get_user(self,create_user1):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)
        check_user = new_account1.get_user()
        assert check_user == new_user1

    def test_request_exist(self,create_user1,create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        new_friends = Relationship.objects.create(sender=new_account1, receiver=new_account2, status='accepted')
        relation = new_account2.request_exist()
        assert relation[0] == new_friends

    def test_check_send_request(self,create_user1,create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        requested = Relationship.objects.create(sender=new_account1, receiver=new_account2, status='send')
        is_request_sent = new_account1.check_send_request()
        assert is_request_sent[0] == new_account2

    def test_check_received_request(self, create_user1, create_user2):
        new_user1 = User.objects.get(username="testuser1")
        new_user1_id = new_user1.id
        new_account1 = Account.objects.get(user_id=new_user1_id)

        new_user2 = User.objects.get(username="testuser2")
        new_user2_id = new_user2.id
        new_account2 = Account.objects.get(user_id=new_user2_id)

        requested = Relationship.objects.create(sender=new_account1, receiver=new_account2, status='send')
        is_request_sent = new_account2.check_received_request()
        assert is_request_sent[0] == new_account1

    def test_get_all_authors_posts(self):
        pass




