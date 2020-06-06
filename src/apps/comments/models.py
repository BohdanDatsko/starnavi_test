from django.db import models
from django.db.models import Index

from apps.posts.models import Post
from common.models import BaseDateAuditModel


class Comment(BaseDateAuditModel):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    comment_body = models.TextField()
    like = models.BigIntegerField(default=0)
    unlike = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

        indexes = [
            Index(fields=["created_at"]),
            Index(fields=["owner", "created_at"]),
            Index(fields=["owner", "post", "created_at"]),
        ]

    def __str__(self):
        return self.comment_body

    def get_comment(self, post_id):
        post = Post.objects.get(id=post_id)
        return f'Comment "{self.comment_body}" has been added to post "{post.title}".'


class CommentLikeUnlike(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    unlike = models.BooleanField(default=False)

    class Meta:
        verbose_name = "CommentLikeUnlike"
        verbose_name_plural = "CommentLikeUnlikes"

        indexes = [
            Index(fields=["owner", "comment"]),
            Index(fields=["owner", "comment", "like"]),
            Index(fields=["owner", "comment", "unlike"]),
            Index(fields=["owner", "comment", "like", "unlike"]),
        ]

    def __str__(self):
        return f"{self.id}"