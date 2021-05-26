from django.db import models

from uuslug import slugify

from decimal import Decimal

#helpers
def get_image_name_category(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.cpu_slug
	return new_name

def get_image_name_picture(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % str(instance.good.cpu_slug)
	return new_name	

#classes
class Good(models.Model):

	title 			= models.CharField(max_length = 150, verbose_name='Наименование')
	fullname 		= models.CharField(max_length = 200, verbose_name='Полное наименование', null=True, blank=True)
	art				= models.CharField(max_length = 10, verbose_name='Артикул', null=True, blank=True)
	description 	= models.TextField(max_length=2048, verbose_name='Описание', blank=True)
	characteristics = models.TextField(max_length=2048, verbose_name='Характеристики', blank=True)
	meta_title 		= models.CharField(max_length=150, verbose_name='meta title', blank=True, null=True)
	meta_description = models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)
	price 			= models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=0, blank=True, null=True)
	is_active		= models.BooleanField(verbose_name='Активен', default=False)
	quantity		= models.DecimalField(verbose_name='Остаток', max_digits=15, decimal_places=0, blank=True, null=True)
	weight			= models.DecimalField(verbose_name='Вес', max_digits=15, decimal_places=2, blank=True, null=True, default='')
	cpu_slug		= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
	good_uid 		= models.CharField(max_length=36, verbose_name='Код 1C', blank=True, null=True)
	category 		= models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)


	def __str__(self):

		return self.title

	def save(self, *args, **kwargs):
		self.title = self.title.upper()
		self.cpu_slug = '{}'.format(slugify(self.title))


		super(Good, self).save(*args, **kwargs)

	def get_pictures(self):
		
		return Picture.objects.filter(good=self)

	def get_main_picture(self):

		main_image = Picture.objects.filter(good=self, main_image=True).first()

		if main_image:

			return main_image

		else:
			
			return Picture.objects.filter(good=self).first()

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


class Category(models.Model):

	title 				= models.CharField(max_length = 150, verbose_name='Наименование')
	meta_title 			= models.CharField(max_length=150, verbose_name='meta title', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)
	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
	uid 				= models.CharField(max_length=36, verbose_name='Код', blank=True, null=True)
	picture				= models.ImageField(upload_to=get_image_name_category, verbose_name='Изображение 270x301', default=None, null=True, blank=True)


	def get_childs(self):
		
		return Category.objects.filter(parent_category=self)

	def __str__(self):

		return self.title

	def save(self, *args, **kwargs):

		self.cpu_slug = '{}'.format(slugify(self.title))	

		super(Category, self).save(*args, **kwargs)

	def get_all_goods(self):
		
		return Good.objects.filter(category=self, is_active=True)

	def get_goods_count(self):
		
		return len(Good.objects.filter(category=self, is_active=True))	

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Picture(models.Model):

	good 					= models.ForeignKey('Good', verbose_name='Товар', on_delete=models.CASCADE)
	images					= models.ImageField(upload_to=get_image_name_picture, verbose_name='Изображение', default=None)
	main_image				= models.BooleanField(verbose_name='Основная картинка', default=False)

	class Meta:
		
		verbose_name = 'Картинка'
		verbose_name_plural = 'Картинки'