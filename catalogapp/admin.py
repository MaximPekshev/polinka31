from django.contrib import admin

from .models import Good, Picture
from .models import Category
from django.utils.safestring import mark_safe

class PictureInline(admin.TabularInline):

   	model = Picture
   	fields =(
				'images',
				'main_image',
		)
   	extra = 0

class GoodAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					'good_uid',
					'price',
					'quantity',
					'weight',
					'is_active',
					'category',
					'image',
					)

	list_filter = ('category',)

	inlines 	 = [PictureInline]

	search_fields = ('title',)

	exclude = ('cpu_slug',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):

		if db_field.name == "category":
			kwargs["queryset"] = Category.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def image(self, obj):

		img = Picture.objects.filter(good=obj, main_image=True).first() if Picture.objects.filter(good=obj, main_image=True).first() else Picture.objects.filter(good=obj).first()
		if img:
			return mark_safe('<img src="{url}" width="50" />'.format(url=img.images.url))
		else:
			return ''	


admin.site.register(Good, GoodAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					)
	
	exclude = ('cpu_slug', )

	search_fields = ('title', )

admin.site.register(Category, CategoryAdmin)