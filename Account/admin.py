from django.contrib import admin
from Account.models import Account, Relationship, SearchHistory

# Register Account and Relationship models with admin
admin.site.register(Account)
admin.site.register(Relationship)
admin.site.register(SearchHistory)
