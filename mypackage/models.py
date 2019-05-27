#Start with chapter 4.4
from mypackage import db

tags = db.Table('tags',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Company(db.Model):
    #snake case naming for table, can use __tablename__ to set manually
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    image_url = db.Column(db.String(128))
    website_url = db.Column(db.String(218))
    product_description = db.Column(db.String(300))
    cause_url = db.Column(db.String(218))
    cause_description = db.Column(db.String(300))
    categories = db.relationship('Category', secondary=tags, backref=db.backref('companies', lazy='dynamic'), lazy='dynamic')
	
    def __repr__(self):
        return '<Company: {}>'.format(self.name)
    
    def is_linked(self, category):
        return self.categories.filter(tags.c.category_id == category.id).count() > 0
    
    def link_category(self, category):
        if not self.is_linked(category):
            self.categories.append(category)
            return True
        else:
            return False
    
    def unlink_category(self, category):
        if self.is_linked(category):
            self.categories.remove(category)
            return True
        else:
            return False

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    parent_id = db.Column(db.String(5), index=True) #set to 0 if top level parent, otherwise set to id of parent

    def __repr__(self):
        return '<Category: {}>'.format(self.name) 