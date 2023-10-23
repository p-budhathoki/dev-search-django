from rest_framework import serializers

from projects.models import Project, Review, Tag
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    # owner field utilizes  ProfileSerializer and returns object
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=False)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
