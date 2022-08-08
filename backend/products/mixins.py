from .models import Product

class UserQuerysetMixin():
    def get_queryset(self): # Get custom query set (Use this to display post in user's profile)
        # qs = super().get_queryset() --> Needs a querry set to be defined in views
        request = self.request
        user = request.user
        qs = Product.objects.filter(user = request.user)
        return qs
        