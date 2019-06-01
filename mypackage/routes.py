from flask import render_template, redirect, jsonify, url_for, flash
from mypackage import app, db
from mypackage.models import Company, Category
from mypackage.forms import CompanyForm, CategoryForm, LinkForm, UnlinkForm

@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.filter_by(parent_id='0').all()
    return render_template('base.html', categories=categories)

@app.route('/filter/<category>')
def category_filter(category):
    category_object = Category.query.filter_by(name=category).first()
    category_id = category_object.id
    parent_id = category_object.parent_id
    companies = category_object.related_companies()
    sub_categories = Category.query.filter_by(parent_id=category_id).all()
    if parent_id == "0":
        return jsonify({'headerdata': render_template('categoryheader.html', sub_categories=sub_categories, category_name=category),
            'bodydata': render_template('categorybody.html', companies=companies)})
    else:
        return jsonify({'bodydata': render_template('categorybody.html', companies=companies)})

################ API's #############################
@app.route('/api/categories/parents', methods=['GET'])
def get_parent_categories():
    category_objects = Category.query.filter_by(parent_id='0').all()
    categories = Category.collection_to_dict(category_objects)
    return jsonify(categories)

@app.route('/api/categories/<category>/sub-categories', methods=['GET'])
def get_sub_categories(category):
    parent_id = Category.query.filter_by(name=category).first().id
    sub_category_objects = Category.query.filter_by(parent_id=parent_id).all()
    sub_categories = Category.collection_to_dict(sub_category_objects)
    return jsonify(sub_categories)

@app.route('/api/categories/<category>/companies', methods=['GET'])
def get_category_companies(category):
    category_object = Category.query.filter_by(name=category).first()
    company_objects = category_object.related_companies()
    companies = Company.collection_to_dict(company_objects)
    return jsonify(companies)

############# Internal data loader ###################
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