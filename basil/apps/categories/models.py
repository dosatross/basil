from django.db import models
from django.db.models import Q

class Category(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	subcategory = models.CharField(max_length=50)
	
	is_credit = models.BooleanField(default=False,null=True) # not negative amount
	is_adjustment = models.BooleanField(default=False) # refund, reimbursement etc.
	is_internal = models.BooleanField(default=False) # transferring money
	is_earned = models.BooleanField(default=None,null=True) # credit not gifted 

	class Meta:
		ordering = ['name','subcategory']

	def get_expense_categories():
		return Category.objects.filter(Q(is_internal=False) 
			& Q(Q(is_credit=False) & Q(is_adjustment=True) 
				| Q(Q(is_credit=True) & Q(is_adjustment=False))))
		# is_internal=False and ((is_credit=False and is_adjustment=True) or (is_credit=True and is_adjustment=False))

	def get_income_categories():
		return Category.objects.filter(Q(is_internal=False) 
			& Q(Q(is_credit=True) & Q(is_adjustment=False) 
				| Q(Q(is_credit=False) & Q(is_adjustment=True))))

	def get_earned_income_categories():
		return self.get_income_categories().filter(is_earned=True)
	
	"""
	categories todo
	- move misc back to reimburse
	- other income

	code todo
	- validate input
	- require category type
	- category model manager?
	

	"""