from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker  , relation , backref


#Configure the data base 
engining = create_engine('mysql://root:02749@localhost:3306/test_fit')
Base = declarative_base()




#Section the table 
class Members(Base):
    __tablename__ =  'members'
    id = Column(Integer, primary_key=True)
    name = Column(String(200) , nullable = True)
    email = Column(String(200) , nullable = True )

    def __repr__(self):
        return "<BooK ( id = '{}' , name = '{}' , email = '{}')>"\
            .format(self.id , self.name , self.email)







#Create table

Base.metadata.drop_all(engining)
Base.metadata.create_all(engining)


Engining = sessionmaker(bind=engining)
session = Engining()


mem1 = Members( id = 1  ,  name = 'Papop' ,  email = 'test123@gmail.com')




session.add(mem1)
session.commit()