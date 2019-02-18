from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Creates the category class with 3 attributes.
# Name, ID, description.
# Provides a JSON API endpoint
class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(1000), nullable=False)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name': self.name,
			'id': self.id,
			'description': self.description
		}

# Creates the Item class with 5 attributes.
# The category_ID is used to as a foreign key to the category class.
# The category field here is used only as a relationship to be used
#when wanting to access the category name from and Item.
# The created_by field is assigned to manage who can edit and delete
#current items in the database. Assigning it here prevents the need 
#for maintaining a user database table, so less risk.
# Provides a JSON API endpoint
class Item(Base):
	__tablename__ = 'item'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(500), nullable = False)
	category_ID = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	created_by = Column(String(100), nullable = False)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'category_ID': self.category_ID,
			'created_by': self.created_by
		}


engine = create_engine('sqlite:///catalog.db')
 

Base.metadata.create_all(engine)
