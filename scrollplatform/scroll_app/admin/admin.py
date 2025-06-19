from django.contrib import admin
from ..models.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(LikesPost)
admin.site.register(CollectPost)
admin.site.register(flowsUser)