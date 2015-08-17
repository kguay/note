# forms.py is used to generate form fields that are used in the
# new_report.html and edit_report.html templates.

import re
# flask
from flask.ext.wtf import Form
from flask.ext.login import current_user
# other
from wtforms import ValidationError, StringField, DateField, DecimalField, FileField, SelectField, TextAreaField, FloatField, IntegerField, BooleanField, SubmitField
from wtforms.validators import Required
from datetime import datetime
from time import gmtime, strftime, localtime
# local
from ..models import Expense

# creat a form for submitting new expense reports.
class ExpenseForm(Form):
    submit_date = StringField('Date Submitted', default=strftime("%m/%d/%Y", localtime()), validators=[Required()])
    purchase_date = StringField('Date Purchased', validators=[Required()])
    vendor = SelectField('Vendor')
    other_vendor = StringField('Other Vendor')
    description = TextAreaField('Description', validators=[Required()])
    amount = StringField('Amount', validators=[Required()])
    account = IntegerField('Account', validators=[Required()])
    receipt = FileField('Receipt', validators=[Required()])
    approved = BooleanField('Approved')
    submit = SubmitField('Submit')
    
    # "validate" currency field (i.e. make valid currency)
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        
        # strip off any non-numeric characters
        non_decimal = re.compile(r'[^\d.]+')
        amount = non_decimal.sub('', self.amount.data)
        
        # try to convert string to numeric (float)
        try:
            amount_float = float(amount)
            # convert back to a string with two decimal places
            self.amount.data = "{0:.2f}".format(amount_float)
        except:
            print('return false')
        
        return True

# creat a form for submitting new expense reports. Almost identical to ExpenseForm.
class EditExpenseForm(Form):
   submit_date = StringField('Date Submitted', validators=[Required()])
   purchase_date = StringField('Date Purchased', validators=[Required()])
   vendor = SelectField('Vendor')
   other_vendor = StringField('Other Vendor')
   description = TextAreaField('Description', validators=[Required()])
   amount = StringField('Amount', validators=[Required()])
   account = IntegerField('Account', validators=[Required()])
   receipt = FileField('Receipt')
   approved = BooleanField('Approved')
   submit = SubmitField('Update')
   
   def __init__(self, expense, *args, **kwargs):
       super(EditExpenseForm, self).__init__(*args, **kwargs)
       self.expense = expense
   
    # "validate" currency field (i.e. make valid currency)
   def validate(self):
       
       # strip off any non-numeric characters
       non_decimal = re.compile(r'[^\d.]+')
       amount = non_decimal.sub('', self.amount.data)
       
       # try to convert string to numeric (float)
       try:
           amount_float = float(amount)
           # convert back to a string with two decimal places
           self.amount.data = "{0:.2f}".format(amount_float)
       except:
           return False
       
       return True