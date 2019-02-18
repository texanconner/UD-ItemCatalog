from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from catalog_db_setup import Category, Item, Base
 

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#soccer
#basketball
#baseball
#frisbee
#snowboarding
#rockclimbing
#skating
#hockey

category1 = Category(name = 'Soccer', description = 'The other football')

session.add(category1)
session.commit()


category2 = Category(name = 'Basketball', description = 'Shooty Hoops')

session.add(category2)
session.commit()

category3 = Category(name = 'Baseball', description = 'Stickball')

session.add(category3)
session.commit()


category4 = Category(name = 'Frisbee', description = 'A sport?')

session.add(category4)
session.commit()

category5 = Category(name = 'Snowboarding', description = 'Cold skateboard')

session.add(category5)
session.commit()

category6 = Category(name = 'Rockclimbing', description = "It's very hard")

session.add(category6)
session.commit()

category7 = Category(name = 'Skating', description = 'Roller Derby kind')

session.add(category7)
session.commit()

category8 = Category(name = 'Hockey', description = 'Ice punching')

session.add(category8)
session.commit()



#Add items
#name
#description
#category
#created_by


#soccer

item1 = Item(name = "Soccer Ball", description = "kick it", category = category1, created_by = 'default')

session.add(item1)
session.commit()

item2 = Item(name = "Soccer Shoes", description = "Feet Gloves", category = category1, created_by = 'default')

session.add(item2)
session.commit()


#Basketball

item3 = Item(name = "Hoop", description = "Round and Orange", category = category2, created_by = 'default')

session.add(item3)
session.commit()


#Baseball


item4 = Item(name = "Bat", description = "Wood stick", category = category3, created_by = 'default')

session.add(item4)
session.commit()


print ("added items!")