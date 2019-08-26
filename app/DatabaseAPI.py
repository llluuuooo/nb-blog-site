from app.models import *
from django.db.models import Max

class BlogData:
    @staticmethod
    def searchBlog(blog_id):
        return Blog.objects.filter(blog_id=blog_id)[0]

    @staticmethod
    def getTags(blog_id):
        blogTags=BlogTag.objects.filter(blog_id=blog_id)
        tags=[]
        if blogTags.count()==0:
            return tags
        for blogTag in blogTags:
            temp=blogTag.tag_id
            tags.append(Tag.objects.filter(tag_id=temp)[0].tag_name)
        return tags

class ReviewData:
    @staticmethod
    def getReviews(blog_id):
        return Review.objects.filter(blog_id=blog_id)

    @staticmethod
    def addReview(blog_id,username,review_time,rev,return_user):
        dict = Review.objects.aggregate(m=Max('review_id'))
        r_id = dict['m'] + 1
        user=UserData.getUserByUsername(username)
        Review.objects.create(review_id=r_id,blog_id=blog_id,user=user,review_time=review_time,review_body=rev,return_user=return_user)

class UserData:
    @staticmethod
    def getUserByUsername(username):
        return Users.objects.filter(user_name=username)[0]
