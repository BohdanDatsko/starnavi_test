from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from starnaviapp.models import Post, Comment, PostLikeUnlike, CommentLikeUnlike

User = get_user_model()


class PostListCreateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.uri1 = "/api/post_create/"
        self.owner = self.setup_user()
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list_post(self):
        response = self.client.get(self.uri)

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create_post(self):
        response = self.client.post(
            self.uri1,
            {
                "owner": self.owner.id,
                "title": "Some post's title",
                "content": "Some post's description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class PostDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/posts/"
        self.uri1 = "/api/post_like_unlike/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Some post's title",
            content="Some post's description",
            owner=self.owner,
        )
        self.test_like_or_unlike = PostLikeUnlike.objects.create(
            owner=self.owner, post=self.test_post, like=False, unlike=False
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_post(self):
        response = self.client.get("{0}{1}/".format(self.uri, self.test_post.pk))

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update_post(self):
        response = self.client.put(
            "{0}{1}/".format(self.uri, self.test_post.pk),
            {
                "owner": self.owner.id,
                "title": "New post's title",
                "content": "New post's description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy_post(self):
        response = self.client.delete("{0}{1}/".format(self.uri, self.test_post.pk))

        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update_post_like_unlike(self):
        response = self.client.post(
            "{0}{1}/".format(self.uri1, self.test_post.pk),
            {"like": True, "unlike": False},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )


class CommentListCreateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/comments/"
        self.uri1 = "/api/comment_create/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Any post's title", content="Any post's description", owner=self.owner
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_list_comment(self):
        response = self.client.get(self.uri)

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_create_comment(self):
        response = self.client.post(
            self.uri1,
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some post's comment",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
            "Expected Response Code 201, received {0} instead.".format(
                response.status_code
            ),
        )


class CommentDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/api/comments/"
        self.uri1 = "/api/comment_like_unlike/"
        self.owner = self.setup_user()
        self.test_post = Post.objects.create(
            title="Any post's title", content="Any post's description", owner=self.owner
        )
        self.test_comment = Comment.objects.create(
            comment_body="Some post's comment", owner=self.owner, post=self.test_post
        )
        self.test_like_or_unlike = CommentLikeUnlike.objects.create(
            owner=self.owner, comment=self.test_comment, like=False, unlike=False
        )
        self.client.force_authenticate(user=self.owner)

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            "Bruce Wayne", email="batman@batcave.com", password="Martha"
        )

    def test_retrieve_comment(self):
        response = self.client.get("{0}{1}/".format(self.uri, self.test_comment.pk))

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update_comment(self):
        response = self.client.put(
            "{0}{1}/".format(self.uri, self.test_comment.pk),
            {
                "owner": self.owner.id,
                "post": self.test_post.id,
                "comment_body": "Some new post's comment",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_destroy_comment(self):
        response = self.client.delete("{0}{1}/".format(self.uri, self.test_comment.pk))

        self.assertEqual(
            response.status_code,
            204,
            "Expected Response Code 204, received {0} instead.".format(
                response.status_code
            ),
        )

    def test_update_comment_like_unlike(self):
        response = self.client.post(
            "{0}{1}/".format(self.uri1, self.test_comment.pk),
            {"like": True, "unlike": False},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Expected Response Code 200, received {0} instead.".format(
                response.status_code
            ),
        )