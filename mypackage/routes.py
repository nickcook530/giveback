from flask import render_template, redirect, jsonify, url_for, flash
from mypackage import app, db
from mypackage.models import Company, Category
from mypackage.forms import CompanyForm, CategoryForm, LinkForm, UnlinkForm

@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.filter_by(parent_id='0').all()
    return render_template('base.html', categories=categories)

@app.route('/fullcategory/<selected_category>', methods=['POST'])
def category_filter(selected_category):
    #categories = Category.query.filter_by(parent_id='0').all()
    selected_id = Category.query.filter_by(name=selected_category).first().id
    sub_categories = Category.query.filter_by(parent_id=str(selected_id)).all()
    companies = Category.query.filter_by(name=selected_category).first().companies
    return jsonify({'headerdata': render_template('categoryheader.html', sub_categories=sub_categories, selected_category=selected_category),
        'bodydata': render_template('categorybody.html', companies=companies)})

@app.route('/subcategory/<selected_sub_category>', methods=['POST'])
def category_sub_filter(selected_sub_category):
    print(selected_sub_category)
    print(type(selected_sub_category))
    companies = Category.query.filter_by(name=selected_sub_category).first().companies
    return jsonify({'bodydata': render_template('categorybody.html', companies=companies)})

@app.route('/dataload', methods=['GET','POST'])
def dataload():
    if not app.debug:
        return redirect(url_for('index'))
    
    #prefix required with multiple forms on same page
    company_form = CompanyForm(prefix="company_form")
    category_form = CategoryForm(prefix="category_form")
    link_form = LinkForm(prefix="link_form")
    unlink_form = UnlinkForm(prefix="unlink_form")
    company_list = Company.query.all()
    category_list = Category.query.all()
    
    if company_form.validate_on_submit():
        company_check = Company.query.filter_by(name=company_form.name.data).first()
        if company_check is not None:
            flash('ERROR: Company already exists!')
            return redirect(url_for('dataload'))
        company = Company(name=company_form.name.data, image_url=company_form.image_url.data, website_url=company_form.website_url.data,
                            product_description=company_form.product_description.data, cause_url=company_form.cause_url.data,
                            cause_description=company_form.cause_description.data)
        db.session.add(company)
        db.session.commit()
        flash('SUCCESS: Company load complete!')
        return redirect(url_for('dataload'))
    
    if category_form.validate_on_submit():
        category_check = Category.query.filter_by(name=category_form.name.data).first()
        if category_check is not None:
            flash('ERROR: Category already exists!')
            return redirect(url_for('dataload'))
        category = Category(name=category_form.name.data, parent_id=category_form.parent_id.data)
        db.session.add(category)
        db.session.commit()
        flash('SUCCESS: Category load complete!')
        return redirect(url_for('dataload'))
        
    if link_form.validate_on_submit():
        company = Company.query.filter_by(id=str(link_form.company_id.data)).first()
        if company is None:
            flash('ERROR: Company you are trying to link does not exist!')
            return redirect(url_for('dataload'))
        category = Category.query.filter_by(id=str(link_form.category_id.data)).first()
        if category is None:
            flash('ERROR: Category you are trying to link does not exist!')
            return redirect(url_for('dataload'))
        if company.link_category(category):
            db.session.commit()
            flash('SUCCESS: Category link to company removed!')
            return redirect(url_for('dataload'))
        else:
            flash('WARNING: Link did not exist!')
            return redirect(url_for('dataload'))
    
    if unlink_form.validate_on_submit():
        company = Company.query.filter_by(id=str(unlink_form.company_id.data)).first()
        if company is None:
            flash('ERROR: Company you are trying to unlink does not exist!')
            return redirect(url_for('dataload'))
        category = Category.query.filter_by(id=str(unlink_form.category_id.data)).first()
        if category is None:
            flash('ERROR: Category you are trying to unlink does not exist!')
            return redirect(url_for('dataload'))
        if company.unlink_category(category):
            db.session.commit()
            flash('SUCCESS: Category link to company removed!')
            return redirect(url_for('dataload'))
        else:
            flash('WARNING: Link did not exist!')
            return redirect(url_for('dataload'))
    
    return render_template('dataload.html', company_form=company_form, category_form=category_form,
                            link_form=link_form, unlink_form=unlink_form, company_list=company_list, category_list=category_list)