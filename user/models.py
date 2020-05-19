import datetime

from django.db import models

class User(models.Model):
        email = models.EmailField(max_length=200, unique=True, null=True)
        nickname = models.CharField(max_length=200, null=True)
        kakao_id = models.IntegerField(unique=True, null=True)
        kakao_name = models.CharField(max_length=200, null=True)
        password = models.CharField(max_length=400, null=True)
        phone_number = models.CharField(max_length=100, unique=True, null=True)
        coupon = models.CharField(max_length=200, null=True)
        account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
        created_at = models.DateTimeField(auto_now_add = True)
        updated_at = models.DateTimeField(auto_now = True, null=True)

        class Meta:
                db_table = 'users'

class Account(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'accounts'

class Energy(models.Model):
	name = models.CharField(max_length=45, default='오늘부터 1일')
	energy = models.IntegerField(default=2000)
	valid_date = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=30))
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	
	class Meta:
		db_table = 'energies'

class UserInterestDetail(models.Model):
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	interest_detail = models.ForeignKey('Interest', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'users_interest_details'

class InterestDetail(models.Model):
	name = models.CharField(max_length=45)
	interest = models.ForeignKey('Interest', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'interest_details'

class Interest(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'interests'

class UserHost(models.Model):
	host = models.ForeignKey('frip.Host', on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'users_hosts'

class UserFrip(models.Model):
	frip = models.ForeignKey('frip.Frip', on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

	class Meta:
		db_table = 'users_frips'

class Review(models.Model):
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	frip = models.ForeignKey('frip.Frip', on_delete=models.SET_NULL, null=True)
	host = models.ForeignKey('frip.Host', on_delete=models.SET_NULL, null=True)
	itinerary = models.ForeignKey('frip.Itinerary', on_delete=models.SET_NULL, null=True)
	option = models.ForeignKey('frip.Option', on_delete=models.SET_NULL, null=True)
	child_option = models.ForeignKey('frip.ChildOption', on_delete=models.SET_NULL, null=True)
	grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		db_table = 'reviews'

class Grade(models.Model):
	number = models.DecimalField(max_digits=5, decimal_places=1)

	class Meta:
		db_table = 'grades'

class Purchase(models.Model):
	user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	frip = models.ForeignKey('frip.Frip', on_delete=models.SET_NULL, null=True)
	itinerary = models.ForeignKey('frip.Itinerary', on_delete=models.SET_NULL, null=True)
	option = models.ForeignKey('frip.Option', on_delete=models.SET_NULL, null=True)
	child_option = models.ForeignKey('frip.ChildOption', on_delete=models.SET_NULL, null=True)
	energy = models.ForeignKey('Energy', on_delete=models.SET_NULL, null=True)
	payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
	review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)
	status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)

	class Meta:
		db_table = 'purchases'

class Status(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'status'

class PaymentMethod(models.Model):
	name = models.CharField(max_length=45)

	class Meta:
		db_table = 'payment_methods'
