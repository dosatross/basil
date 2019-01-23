from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class CategoryGroup(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150, null=True)

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	subcategory = models.CharField(max_length=50)
	groups = models.ManyToManyField(CategoryGroup, related_name='categories')
	
	is_credit = models.BooleanField(default=False,null=True) 	# not negative amount
	is_adjustment = models.BooleanField(default=False) 			# refund, reimbursement etc.
	is_internal = models.BooleanField(default=False) 			# transferring money

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['name','subcategory']

	def __str__(self):
		return '%s - %s' % (self.name, self.subcategory)

	def get_expense_categories():
		return Category.objects.filter(Q(is_internal=False)		  # remove internals
			& Q(Q(is_credit=False) 								  # get debits
				| Q(Q(is_credit=True) & Q(is_adjustment=True))))  # get credit adjustments
	def get_income_categories():
		return Category.objects.filter(Q(is_internal=False) 	  # remove internals
			& Q(Q(is_credit=True) 								  # get credits
				| Q(Q(is_credit=False) & Q(is_adjustment=True)))) # get debit adjustments