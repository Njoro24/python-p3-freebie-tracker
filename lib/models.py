# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy import select
from typing import List

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = 'companies'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    founding_year: Mapped[int] = mapped_column(Integer)
    
    # Relationship to freebies
    freebies: Mapped[List["Freebie"]] = relationship(back_populates='company')
    
    def __repr__(self):
        return f'<Company {self.name}>'
    
    @property
    def devs(self):
        """Returns a collection of all devs who collected freebies from this company"""
        return [freebie.dev for freebie in self.freebies]
    
    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie instance associated with this company and the given dev"""
        new_freebie = Freebie(
            dev=dev,
            company=self,
            item_name=item_name,
            value=value
        )
        return new_freebie
    
    @classmethod
    def oldest_company(cls):
        """Returns the oldest company based on founding_year"""
        engine = create_engine('sqlite:///freebies.db')
        Session = sessionmaker(bind=engine)
    
        with Session() as session:
            stmt = select(cls).order_by(cls.founding_year.asc())
            return session.execute(stmt).scalars().first()

class Dev(Base):
    __tablename__ = 'devs'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    
    # Relationship to freebies
    freebies: Mapped[List["Freebie"]] = relationship(back_populates='dev')
    
    def __repr__(self):
        return f'<Dev {self.name}>'
    
    @property
    def companies(self):
        """Returns a collection of all companies that the Dev has collected freebies from"""
        return [freebie.company for freebie in self.freebies]
    
    def received_one(self, item_name):
        """Returns True if any of the freebies associated with the dev has that item name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, dev, freebie):
        """Changes the freebie's dev to be the given dev if the freebie belongs to this dev"""
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String)
    value: Mapped[int] = mapped_column(Integer)
    
    # Foreign keys
    dev_id: Mapped[int] = mapped_column(ForeignKey('devs.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
    
    # Relationships
    dev: Mapped["Dev"] = relationship(back_populates='freebies')
    company: Mapped["Company"] = relationship(back_populates='freebies')
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        """Returns a formatted string with freebie details"""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."

# Database setup function
def create_tables():
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    return engine

# Example usage and testing
if __name__ == "__main__":
    # Create database and tables
    engine = create_tables()
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Create sample data
        company1 = Company(name="Google", founding_year=1998)
        company2 = Company(name="Microsoft", founding_year=1975)
        company3 = Company(name="Apple", founding_year=1976)
        
        dev1 = Dev(name="Alice")
        dev2 = Dev(name="Bob")
        dev3 = Dev(name="Charlie")
        
        # Add to session
        session.add_all([company1, company2, company3, dev1, dev2, dev3])
        session.commit()
        
        # Create freebies
        freebie1 = Freebie(item_name="T-shirt", value=25, dev=dev1, company=company1)
        freebie2 = Freebie(item_name="Stickers", value=5, dev=dev1, company=company2)
        freebie3 = Freebie(item_name="Water Bottle", value=15, dev=dev2, company=company1)
        freebie4 = Freebie(item_name="Laptop Bag", value=50, dev=dev3, company=company3)
        
        session.add_all([freebie1, freebie2, freebie3, freebie4])
        session.commit()
        
        # Test the methods
        print("=== Testing Relationships ===")
        print(f"Dev1 freebies: {[f.item_name for f in dev1.freebies]}")
        print(f"Dev1 companies: {[c.name for c in dev1.companies]}")
        print(f"Company1 freebies: {[f.item_name for f in company1.freebies]}")
        print(f"Company1 devs: {[d.name for d in company1.devs]}")
        
        print("\n=== Testing Methods ===")
        print(f"Freebie1 details: {freebie1.print_details()}")
        print(f"Dev1 received T-shirt: {dev1.received_one('T-shirt')}")
        print(f"Dev1 received Laptop: {dev1.received_one('Laptop')}")
        
        # Test give_freebie
        new_freebie = company2.give_freebie(dev2, "Mouse Pad", 10)
        session.add(new_freebie)
        session.commit()
        print(f"New freebie created: {new_freebie.print_details()}")
        
        # Test give_away
        print(f"Before give_away - Freebie1 owner: {freebie1.dev.name}")
        dev1.give_away(dev2, freebie1)
        session.commit()
        print(f"After give_away - Freebie1 owner: {freebie1.dev.name}")
        
        # Test oldest_company
        oldest = Company.oldest_company()
        if oldest:
            print(f"Oldest company: {oldest.name} (founded {oldest.founding_year})")
        
        session.commit()