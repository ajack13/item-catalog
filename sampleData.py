from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Genre, Base, Albums,User
 
engine = create_engine('sqlite:///music_store.db')
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

#Menu for UrbanBurger
genre1 = Genre(name = "Rock" ,user_id="a@g.com")

session.add(genre1)
session.commit()


item1 = Albums(name = "ACDC", 
				description = "Poster of acdc", 
				price = "$2.99", 
				p_type = "Posters & Art",
				genre = genre1 ,
				img_name='acdc.jpg',
				user_id="a@g.com")

session.add(item1)
session.commit()

item2 = Albums(name = "Nevermind", 
				description = "The greatest rock album of the past century Nevermind is the second studio album by the American rock band Nirvana, released on September 24, 1991", 
				price = "$10.99", 
				p_type = "Album",
				genre = genre1 ,
				img_name='nevermind.jpg',
				user_id="a@g.com")

session.add(item2)
session.commit()

item3 = Albums(name = "Aerosmith", 
				description = "guitar used by famous aerosmith lead guitarist Joe perry", 
				price = "$200.99", 
				p_type = "Collectables",
				genre = genre1 ,
				img_name='aero.jpg',
				user_id="a@g.com")

session.add(item3)
session.commit()

item4 = Albums(name = "Metallica", 
				description = "Metallica is an American heavy metal band formed in Los Angeles, California. Metallica was formed in 1981", 
				price = "$15.99", 
				p_type = "Poster & Art",
				genre = genre1 ,
				img_name='metallica.jpg',
				user_id="a@g.com")

session.add(item4)
session.commit()

item5 = Albums(name = "Queen", 
				description = "Queen are a British rock band that formed in London in 1970. The classic line-up was Freddie Mercury, Brian May, Roger Taylor, and John Deacon", 
				price = "$20.99", 
				p_type = "Album",
				genre = genre1 ,
				img_name='queen.jpg',
				user_id="a@g.com")

session.add(item5)
session.commit()

item6 = Albums(name = "Marilyn Manson", 
				description = "Marilyn Manson is an American rock band from Fort Lauderdale, Florida. Formed in 1989 by frontman Marilyn Manson and Daisy Berkowitz", 
				price = "$20.99", 
				p_type = "Album",
				genre = genre1 ,
				img_name='manson.jpg',
				user_id="a@g.com")

session.add(item6)
session.commit()

item6 = Albums(name = "Guns N Roses", 
				description = "Guns N' Roses is an American hard rock band from Los Angeles formed in 1985", 
				price = "$20.99", 
				p_type = "Collectables",
				genre = genre1 ,
				img_name='gnr.jpg',
				user_id="a@g.com")

session.add(item6)
session.commit()


