from django.db import models

class Frip(models.Model):
	title = models.CharField(max_length=200)
	catch_phrase = models.CharField(max_length=300)
	price= models.IntegerField()
	faked_price = models.IntegerField()
	duedate = models.IntegerField()
	location = models.CharField(max_length=300)
	venue = models.CharField(max_length=1000)
	venue_lng = models.DecimalField(max_digits=10, decimal_places=6)
	venue_lat = models.DecimalField(max_digits=10, decimal_places=6)
	gathering_place = models.CharField(max_length=1000)
	geopoint_lng = models.DecimalField(max_digits=10, decimal_places=6)
	geopoint_lat = models.DecimalField(max_digits=10, decimal_places=6)
	today = models.BooleanField()
	ticket = models.BooleanField()
	sale = models.BooleanField(default=0)
	dateValidFrom = models.DateTimeField()
	dateValidTo = models.DateTimeField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()
	host = models.ForeignKey('Host', on_delete=models.SET_NULL, null=True)
	detail = models.OneToOneField('Detail', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'frips'

class Detail(models.Model):
	content = models.TextField()
	include = models.TextField()
	exclude = models.TextField()
	schedule = models.TextField()
	material = models.TextField()
	notice = models.TextField()

	class Meta:
		db_table = 'details'

class Image(models.Model):
	image_url = models.URLField(max_length=2000)
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'images'

class Itinerary(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	max_quantity = models.IntegerField()
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	option = models.ManyToManyField('Option', through='ItineraryOption')

	class Meta:
		db_table = 'itineraries'

class Option(models.Model):
	name = models.CharField(max_length=200)
	price = models.IntegerField()
	base_price = models.IntegerField()
	max_quantity = models.IntegerField()
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	option_type = models.OneToOneField('OptionType', on_delete=models.SET_NULL, null=True)
	child_option = models.ManyToManyField('ChildOption', through = 'OptionChildOption')

	class Meta:
		db_table = 'options'

class ChildOption(models.Model):
    name = models.CharField(max_length=45)
    price = models.IntegerField()
    base_price = models.IntegerField()
    frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
    option_type = models.OneToOneField('OptionType', on_delete=models.SET_NULL, null=True)
	
    class Meta:
        db_table = 'child_options'

class ItineraryOption(models.Model):
	itinerary = models.ForeignKey('Itinerary', on_delete=models.SET_NULL, null=True)
	option = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'itineraries_options'

class OptionChildOption(models.Model):
	option = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True)
	child_option = models.ForeignKey('ChildOption', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'options_child_options'

class OptionType(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'option_types'

class MainTab(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'main_tabs'

class FirstCategory(models.Model):
	name = models.CharField(max_length=45)
	main_tab = models.ForeignKey('MainTab', on_delete=models.SET_NULL, null=True)
	frip = models.ManyToManyField('Frip', through='FripCategory')

	class Meta:
		db_table = 'first_categories'

class SecondCategory(models.Model):
	name = models.CharField(max_length=45)
	first_category = models.ForeignKey('FirstCategory', on_delete=models.SET_NULL, null=True)
	frip = models.ManyToManyField('Frip', through='FripCategory')
	
	class Meta:
		db_table = 'second_categories'

class ThirdCategory(models.Model):
	name = models.CharField(max_length=45)
	second_category = models.ForeignKey('SecondCategory', on_delete=models.SET_NULL, null=True)
	frip = models.ManyToManyField('Frip', through='FripCategory')
	class Meta:
		db_table = 'third_categories'

class FourthCategory(models.Model):
	name = models.CharField(max_length=45)
	third_category = models.ForeignKey('ThirdCategory', on_delete=models.SET_NULL, null=True)
	frip = models.ManyToManyField('Frip', through='FripCategory')

	class Meta:
		db_table = 'fourth_categories'

class FripCategory(models.Model):
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	first_category = models.ForeignKey('FirstCategory', on_delete=models.SET_NULL, null=True)
	second_category = models.ForeignKey('SecondCategory', on_delete=models.SET_NULL, null=True)
	third_category = models.ForeignKey('ThirdCategory', on_delete=models.SET_NULL, null=True)
	fourth_category = models.ForeignKey('FourthCategory', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'frips_categories'

class Host(models.Model):
	name = models.CharField(max_length=200)
	image_url = models.URLField(max_length=2000)
	description = models.TextField()
	super_host = models.BooleanField()

	class Meta:
		db_table = 'hosts'

class Event(models.Model):
	image_url = models.URLField(max_length=2000)
	frip = models.ManyToManyField('Frip', through='FripEvent')

	class Meta:
		db_table = 'events'

class FripEvent(models.Model):
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'frips_evnets'

class Theme(models.Model):
	name = models.CharField(max_length=200)
	frip = models.ManyToManyField('Frip', through='FripTheme')
	
	class Meta:
		db_table = 'themes'

class FripTheme(models.Model):
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'frips_themes'

class Region(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'regions'

class SubRegion(models.Model):
    name = models.CharField(max_length=45)
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True)
    frip = models.ManyToManyField('Frip', through='FripSubRegion')

    class Meta:
        db_table = 'sub_regions'

class FripSubRegion(models.Model):
	frip = models.ForeignKey('Frip', on_delete=models.SET_NULL, null=True)
	sub_region = models.ForeignKey('SubRegion', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'frips_sub_regions'
