from django.contrib import admin
from cab.models import Snippet, Language, Bookmark


class SnippetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Snippet)

class LanguageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Language, LanguageAdmin)

class BookmarkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bookmark, BookmarkAdmin)




