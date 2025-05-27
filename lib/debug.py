#!/usr/bin/env python3
# debug.py

# Handle ipdb import gracefully
try:
    import ipdb
    debugger = ipdb
    print("Using ipdb for debugging")
except ImportError:
    import pdb
    debugger = pdb
    print("ipdb not available, using built-in pdb")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models with error handling
try:
    from models import Company, Dev, Freebie, Base
    print("Successfully imported models")
except Exception as e:
    print(f"Error importing models: {e}")
    print("Make sure your models.py file has the 'extend_existing=True' fix applied")
    exit(1)

def main():
    try:
        # Set up database connection
        engine = create_engine('sqlite:///freebies.db', echo=False)
        
        # Try to create tables (this might fail if models have issues)
        print("Creating database tables...")
        Base.metadata.create_all(engine)
        print("Database tables created successfully")
        
        Session = sessionmaker(bind=engine)
        
        with Session() as session:
            # Get some sample data to work with
            try:
                companies = session.query(Company).all()
                devs = session.query(Dev).all()
                freebies = session.query(Freebie).all()
            except Exception as e:
                print(f"Error querying database: {e}")
                print("Database might be empty or corrupted. Try running seed.py first.")
                companies, devs, freebies = [], [], []
            
            print("=== Welcome to the Freebie Debug Console ===")
            print(f"Available data:")
            print(f"  Companies: {len(companies)} - {[c.name for c in companies[:3]] if companies else 'None'}")
            print(f"  Developers: {len(devs)} - {[d.name for d in devs[:3]] if devs else 'None'}")
            print(f"  Freebies: {len(freebies)} - {[f.item_name for f in freebies[:3]] if freebies else 'None'}")
            print()
            
            # Make some variables available for debugging
            company = companies[0] if companies else None
            dev = devs[0] if devs else None
            freebie = freebies[0] if freebies else None
            
            if company:
                print(f"Sample company: {company.name}")
            if dev:
                print(f"Sample dev: {dev.name}")
            if freebie:
                print(f"Sample freebie: {freebie.item_name}")
            
            if not any([companies, devs, freebies]):
                print("No data found in database. Consider running seed.py first.")
                print()
                print("You can still explore the models and create test data:")
                print("  new_company = Company(name='Test Co', founding_year=2020)")
                print("  session.add(new_company)")
                print("  session.commit()")
            
            print()
            print("Available variables in debug session:")
            print("  session    # Database session")
            print("  Company    # Company model class")
            print("  Dev        # Dev model class") 
            print("  Freebie    # Freebie model class")
            print("  company    # Sample company instance (if available)")
            print("  dev        # Sample dev instance (if available)")
            print("  freebie    # Sample freebie instance (if available)")
            print()
            print("Try these commands:")
            if dev:
                print(f"  dev.freebies  # See all freebies for {dev.name}")
                if hasattr(dev, 'companies'):
                    print(f"  dev.companies  # See all companies {dev.name} has freebies from")
            if company:
                print(f"  company.freebies  # See all freebies from {company.name}")
                if hasattr(company, 'devs'):
                    print(f"  company.devs  # See all devs who have freebies from {company.name}")
            if freebie and hasattr(freebie, 'print_details'):
                print("  freebie.print_details()  # Print freebie details")
            if dev and hasattr(dev, 'received_one'):
                print("  dev.received_one('T-shirt')  # Check if dev has a specific item")
            if hasattr(Company, 'oldest_company'):
                print("  Company.oldest_company()  # Get the oldest company")
            print("  session.query(Company).all()  # Get all companies")
            print("  session.query(Dev).all()     # Get all developers")
            print("  session.query(Freebie).all() # Get all freebies")
            print()
            
            # Start debug session
            print("Starting debug session... (type 'c' to continue, 'q' to quit)")
            debugger.set_trace()
            
    except Exception as e:
        print(f"Error in main: {e}")
        print("This might be due to the table definition issue mentioned in your error.")
        print("Make sure to add 'extend_existing=True' to your model __table_args__")
        return

if __name__ == "__main__":
    main()