from django_filters import rest_framework as rfilters
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api import services
from apps.api.serializers import (
    PostSerializer,
    PostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    FanSerializer,
    LikeSerializer,
)
from apps.comments.models import Comment
from apps.posts.models import Post
from apps.reactions.models import Like


class PostListApiView(GenericViewSet, ListAPIView):
    """
        PostListApiView.
        Users can see all posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "pub_date"]


class PostCreateApiView(GenericViewSet, CreateAPIView):
    """
        PostCreateApiView.
        Authorized users can also add new posts
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        PostDetailApiView.
        Authorized users can update or delete their posts
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "post_pk"

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)

        return response


class CommentListApiView(GenericViewSet, ListAPIView):
    """
        CommentList.
        Users can see all post's comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter, rfilters.DjangoFilterBackend]
    filterset_fields = ("post",)
    ordering_fields = ["post"]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("post_pk", None))


class CommentCreateApiView(GenericViewSet, CreateAPIView):
    """
        CommentCreateApiView.
        Authorized users can also add new comments to posts
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, post_id=self.kwargs.get("post_pk", None))


class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    """
        CommentDetail.
        Authorized users can update or delete their comments
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "comment_pk"

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data["owner"] = self.request.user.id
        response = super().update(request, *args, **kwargs)

        return response


class PostLikeUnlikeApiView(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "post_pk"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs.get("post_pk", None))

    @action(methods=["POST"], detail=True)
    def like(self, request, **kwargs):
        """
        Likes "obj".
        """
        obj = self.get_object()
        services.add_like(obj, request.user)

        return Response(f'You have just liked "{obj}"')

    @action(methods=["POST"], detail=True)
    def unlike(self, request, **kwargs):
        """
        Remove like from "obj".
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)

        return Response(f'You have just removed your like from "{obj}"')

    @action(detail=False)
    def fans(self, request, **kwargs):
        """
        Get all users which have liked "obj".
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)


class CommentLikeUnlikeApiView(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "comment_pk"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs.get("comment_pk", None))

    @action(methods=["POST"], detail=True)
    def like(self, request, **kwargs):
        """
        Likes "obj".
        """
        obj = self.get_object()
        services.add_like(obj, request.user)

        return Response(f'You have just liked "{obj}"')

    @action(methods=["POST"], detail=True)
    def unlike(self, request, **kwargs):
        """
        Remove like from "obj".
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response(f'You have just removed your like from "{obj}"')

    @action(detail=False)
    def fans(self, request, **kwargs):
        """
        Get all users which have liked "obj".
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)

        return Response(serializer.data)
