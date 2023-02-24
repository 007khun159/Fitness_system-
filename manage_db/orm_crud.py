from sqlalchemy import Column, Integer, String,Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker  , relation , backref


#Configure the data base 
engining = create_engine('mysql://root:02749@localhost:3306/fitness')
Base = declarative_base()




#Section the table 
class Members(Base):
    __tablename__ =  'members'
    id = Column(Integer, primary_key=True)
    username  = Column(String(200) , nullable = True)
    password = Column(String(200) , nullable  = False)
    email = Column(String(200) , nullable = True )

    def __repr__(self):
        return "<Member ( id = '{}' , username = '{}' ,password = '{}', email = '{}')>"\
            .format(self.id , self.username ,self.password, self.email)




class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return "<Product(id='{}', name='{}', price='{}')>"\
            .format(self.id, self.name, self.price)










#Create table

Base.metadata.drop_all(engining)
Base.metadata.create_all(engining)


Engining = sessionmaker(bind=engining)
session = Engining()


mem1 = Members( id = 1  ,  username  = 'deaw' ,password = '123',  email = 'test123@gmail.com')


product1 = Product(id = 1 , name = " 1 Month " , price = 300.50)


list_infor = [mem1 , product1]


for i in list_infor:
    session.add(i)






session.commit()