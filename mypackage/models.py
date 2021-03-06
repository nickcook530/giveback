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
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
            'website_url': self.website_url,
            'product_description': self.product_description,
            'cause_url': self.cause_url,
            'cause_description': self.cause_description,
            'categories': 'INPUT url_for of API'
        }
        return data
    
    @staticmethod
    def collection_to_dict(collection):
        list_of_dict = []
        for query_object in collection:
            list_of_dict.append(query_object.to_dict())
        return list_of_dict

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    parent_id = db.Column(db.Integer, index=True) #set to 0 if top level parent, otherwise set to id of parent

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
    
    def related_companies(self):
        companies = Company.query.join(tags,(tags.c.company_id==Company.id)).order_by(Company.name).filter(tags.c.category_id==self.id).all()
        return companies
    
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'companies': 'INPUT url_for of API'
        }
        return data

    @staticmethod
    def collection_to_dict(collection):
        list_of_dict = []
        for query_object in collection:
            list_of_dict.append(query_object.to_dict())
        return list_of_dict