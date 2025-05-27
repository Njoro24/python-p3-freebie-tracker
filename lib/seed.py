# seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

def seed_data():
    # Create engine and session
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Clear existing data
        session.query(Freebie).delete()
        session.query(Dev).delete()
        session.query(Company).delete()
        session.commit()
    
    # Create companies
    google = Company(name="Google", founding_year=1998)
    microsoft = Company(name="Microsoft", founding_year=1975)
    apple = Company(name="Apple", founding_year=1976)
    meta = Company(name="Meta", founding_year=2004)
    amazon = Company(name="Amazon", founding_year=1994)
    
    # Create developers
    alice = Dev(name="Alice Johnson")
    bob = Dev(name="Bob Smith")
    charlie = Dev(name="Charlie Brown")
    diana = Dev(name="Diana Prince")
    eve = Dev(name="Eve Wilson")
    
    # Add to session
    session.add_all([google, microsoft, apple, meta, amazon])
    session.add_all([alice, bob, charlie, diana, eve])
    session.commit()
    
    # Create freebies
    freebies = [
        Freebie(item_name="Google T-shirt", value=25, dev=alice, company=google),
        Freebie(item_name="Google Stickers", value=5, dev=alice, company=google),
        Freebie(item_name="Microsoft Water Bottle", value=15, dev=bob, company=microsoft),
        Freebie(item_name="Apple USB-C Cable", value=30, dev=charlie, company=apple),
        Freebie(item_name="Meta VR Headset", value=200, dev=diana, company=meta),
        Freebie(item_name="Amazon Echo Dot", value=50, dev=eve, company=amazon),
        Freebie(item_name="Microsoft Mouse Pad", value=10, dev=alice, company=microsoft),
        Freebie(item_name="Google Hoodie", value=45, dev=bob, company=google),
        Freebie(item_name="Apple AirPods", value=150, dev=charlie, company=apple),
        Freebie(item_name="Meta Portal", value=100, dev=alice, company=meta),
    ]
    
    session.add_all(freebies)
    session.commit()
        
    print("Database seeded successfully!")
    print(f"Created {len(session.query(Company).all())} companies")
    print(f"Created {len(session.query(Dev).all())} developers")
    print(f"Created {len(session.query(Freebie).all())} freebies")

if __name__ == "__main__":
    seed_data()