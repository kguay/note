# views.py renders pages for creating, editing, reviewing, and approving
# expense reports.

import os
# flask
from flask.ext.login import current_user, logout_user, login_required
from flask_wtf.file import FileField
from flask import Flask, render_template, redirect, request, url_for, flash, send_from_directory, send_file
# other
from werkzeug import secure_filename
from datetime import datetime, date
from sqlalchemy import desc, asc
# local
from . import main
from .. import db
from .forms import ExpenseForm, EditExpenseForm
from ..decorators import admin_required, permission_required
from ..models import Expense, load_expenses, User, Vendor

# settins for file upload (not used in current version)
UPLOAD_FOLDER = '/receipts'
ALLOWED_EXTENSIONS = set(['pdf'])


@main.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('main.review'))
    else:
        return redirect(url_for('auth.login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# This view is used to create new expense reports. 
# new_report.html
@main.route('/new_report', methods=['GET','POST'])
@login_required
def new_report():
    form = ExpenseForm()
    form.vendor.choices = [(v.name, v.name) for v in Vendor.query.order_by('name')] + [('Other','Other')]
    
    # make sure that the form is complete & valid
    if form.validate_on_submit():
        
        # if a custom vendor was added, save it to the 'vendors' table
        if (form.vendor.data == 'Other'):
            if (form.other_vendor.data == "Other") or (form.other_vendor.data == ""):
               form.vendor.data = "Other"
            else:
               vendor = Vendor(name=form.other_vendor.data)
               db.session.add(vendor)
               form.vendor.data = form.other_vendor.data
        
        # Get the data from the form and store it in new instance of Expense
        expense = Expense(user_id=current_user.id,
                       username=current_user.full_name,
                       submit_date=form.submit_date.data,
                       purchase_date=form.purchase_date.data,
                       vendor=form.vendor.data,
                       description=form.description.data,
                       amount=form.amount.data,
                       account=form.account.data,
                       approved=0)
                
        # submit to database in order to get expense id to use in filename
        db.session.add(expense)
        db.session.commit()

        # get the id of the expense just submitted -- no longer needed,
        #  but kept in case
        #expense = Expense.query.filter_by(user_id=current_user.id).last()
        #print(expense.id)
        
        # Get the name of the uploaded file
        file = request.files['receipt']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            filename = '/receipts/' + current_user.username + '/' + current_user.username + '_' + str(int(expense.id)) + '.pdf'
            full_filename = 'app/static' + filename
            full_dir = 'app/static/receipts/' + current_user.username + '/'
            
            # check if the directory exists. If so, save the file.
            #  Otherwise, make the directory before saving the file
            if os.path.isdir(full_dir):
                file.save(full_filename)
            else:
                os.makedirs(full_dir)
                file.save(full_filename)
            
            # save the filename to expense.receipt
            expense.receipt = filename
            db.session.commit()
        
        flash('Expense report submitted')
        # go to review (home)
        return redirect(url_for('main.review'))
    
    else:
        if request.method=='POST':
            flash('Please complete all fields and select receipt file before submitting.')
    
    name = current_user.full_name
    return render_template('new_report.html', form=form, name=name)

# This view is used to edit expense reports. 
# edit_report.html
@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    expense = Expense.query.get_or_404(id)
    form = EditExpenseForm(expense=expense)
    
    # make sure that the form is complete & valid
    if form.validate_on_submit():
        
        # if a custom vendor was added, save it to the 'vendors' table
        if (form.vendor.data == 'Other'):
            if (form.other_vendor.data == "Other") or (form.other_vendor.data == ""):
               form.vendor.data = "Other"
            else:
               vendor = Vendor(name=form.other_vendor.data)
               db.session.add(vendor)
               form.vendor.data = form.other_vendor.data
        
        # if the user uploaded a new receipt, save it in place of the old one (rewrite)
        if form.receipt.data:
            # Get the name of the uploaded file
            file = request.files['receipt']
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to
                # the upload folder we setup
                filename = '/receipts/' + current_user.username + '/' + current_user.username + '_' + str(int(expense.id)) + '.pdf'
                full_filename = 'app/static' + filename
                full_dir = 'app/static/receipts/' + current_user.username + '/'
                
                file.save(full_filename)
        
        # update the expense object with the form data
        expense.submit_date=form.submit_date.data
        expense.purchase_date=form.purchase_date.data
        expense.vendor=form.vendor.data
        expense.description=form.description.data
        expense.amount=form.amount.data
        expense.account=form.account.data
        expense.approved=form.approved.data
        
        # submit to database
        db.session.add(expense)
        
        flash('Expense report updated')
        return redirect(request.args.get('next') or url_for('main.review'))
    
    # populate the edit_report.html with data from expense table
    name = expense.username
    form.submit_date.data = expense.submit_date
    form.purchase_date.data = expense.purchase_date
    form.vendor.data = expense.vendor
    form.description.data = expense.description
    form.amount.data = '$'+expense.amount
    form.account.data = expense.account
    form.receipt.data = expense.receipt
    form.approved.data = expense.approved
    
    # add vendor choices from 'vendors' table
    form.vendor.choices = [(v.name, v.name) for v in Vendor.query.order_by('name')] + [('Other','Other')]
    
    return render_template('edit_report.html', form=form, expense=expense, name=name)
    

# Create a print view for the selected expense (id)
@main.route('/print/<int:id>', methods=['GET'])
@login_required
def print_report(id):
    # get the expense based on the id (if one exists)
    expense = Expense.query.get_or_404(id)
    
    return render_template('print.html', expense=expense)

# Approve an expense (admin only)
@main.route('/app/<int:id>', methods=['GET','POST'])
@login_required
def app(id):
    # load the expense form id (if one exists)
    expense = Expense.query.get_or_404(id)
    # set approved to the user's (supervisor's) id
    # this way, you know who approved your expense report (to be implemented)
    expense.approved = current_user.id
    # updated expenses table
    db.session.add(expense)
    # go back to approve.html with hide and sort arguements maintained
    return redirect("/approve?hide=" + request.args.get('hide') + "&sort=" + request.args.get('sort'))

# Unapprove an expense (admin only)
@main.route('/unapp/<int:id>', methods=['GET','POST'])
@login_required
def unapp(id):
    # load the expense form id (if one exists)
    expense = Expense.query.get_or_404(id)
    # set approved to 0 (not approved)
    expense.approved = 0
    # updated expenses table
    db.session.add(expense)
    # go back to approve.html with hide and sort arguements maintained
    return redirect("/approve?hide=" + request.args.get('hide') + "&sort=" + request.args.get('sort'))

# Delete an expense (must click button twice to avoid accidental delete)
@main.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    # load the expense form id (if one exists)
    expense = Expense.query.get_or_404(id)
    # delete row
    db.session.delete(expense)
    # update table
    db.session.commit()
    # return to the page the the user came from (review or approve).
    # (review if not specified)
    if request.args.get('next'):
       return redirect(request.args.get('next') or url_for('main.review'))
    else:
       return redirect(url_for('main.review'))

# Review all of the current user's reports. Edit and print options available
# from this page
@main.route('/review')
@login_required
def review():
    # get sort arg for orderby
    if request.args.get('sort'):
        orderby = request.args.get('sort')
    else:
        orderby = 'timestamp desc'
    
    # get expenses and sory according to sort arg or date
    e = Expense.query.filter_by(user_id=current_user.id).order_by(orderby).all()

    # return to the page the the user came from (review or approve).
    # (review if not specified)
    return render_template('review.html', data=e, orderby=orderby)

# Approve reports from all users. Edit, print, and approve from this page.
@main.route('/approve')
@login_required
def approve():
    # get sort arg for orderby
    if request.args.get('sort'):
        orderby = request.args.get('sort').split()
    else:
        orderby = 'timestamp desc'.split()
    
    # get expenses from 'expenses' table. Hide (default) or show reports that
    # have already been approved
    if request.args.get('hide') == "False":
        if orderby[1] == 'asc':
           e = Expense.query.order_by(asc(orderby[0])).all()
        else:
           e = Expense.query.order_by(desc(orderby[0])).all()
        hide=False
    else:
        if orderby[1] == 'asc':
           e = Expense.query.filter_by(approved=0).order_by(asc(orderby[0])).all()
        else:
           e = Expense.query.filter_by(approved=0).order_by(desc(orderby[0])).all()
        hide=True

    
    ###  N E E D   T O   R E M O V E ###
    #e = Expense.query.order_by(orderby)
    ####################################
        
    # count the number of rows that are hidden
    hidden = Expense.query.count() - Expense.query.filter_by(approved=0).count()
    
    return render_template('approve.html', data=e, hide=hide, hidden=hidden, orderby=" ".join(orderby))
    
# Render FAQ page
@main.route('/faq')
def faq():
    return render_template('faq.html')