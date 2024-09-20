from sqlalchemy import create_engine, Column, String, Numeric, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import func


# Define Classes/Tables
class Base(DeclarativeBase):
    pass


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    laddress: Mapped[str] = mapped_column(String(30))
    lphone: Mapped[str] = mapped_column(String(30))
    mgrid: Mapped[str] = mapped_column(String(10))
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="location"
    )

    def __repr__(self) -> str:  # represents the object as a string
        return f"Location(id={self.id!r}, laddress={self.laddress!r}, lphone={self.lphone!r}, mgrID={self.mgrID!r})"


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    ename: Mapped[str] = mapped_column(String(40))
    esalary: Mapped[int] = mapped_column(Integer)
    etitle: Mapped[str] = mapped_column(String(40))
    storeid: Mapped[str] = mapped_column(String(40), ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship(back_populates="employees")

    def __repr__(self) -> str:
        return f"Employee(id={self.id!r}, ename={self.ename!r}, esalary={self.esalary!r}, etitle={self.etitle!r})"


# Create Tables
Base.metadata.create_all(engine)

# Insert Data
with Session(engine) as session:
    Chicago = Location(
        id="001",
        laddress="123 Chicago, IL 60660",
        lphone="1234567890",
        mgrid="101",
        employees=[
            Employee(id="101", ename="Keren Madhur", esalary=82000, etitle="manager"),
            Employee(id="102", ename="Lamis Hugo", esalary=20000, etitle="sales associate"),
            Employee(id="103", ename="Bose Zoriana", esalary=25000, etitle="sales associate"),
            Employee(id="104", ename="Vittore Isobel", esalary=30000, etitle="sales associate")
        ]
    )
    NewYork = Location(
        id="002",
        laddress="222 New York, NY 10001",
        lphone="9876543210",
        mgrid="201",
        employees=[
            Employee(id="201", ename="Carlota Andromache", esalary=84000, etitle="manager", storeid="002"),
            Employee(id="202", ename="Isi Adrian", esalary=28000, etitle="sales associate", storeid="002"),
            Employee(id="203", ename="Hendrikus Mislav", esalary=40000, etitle="sales associate", storeid="002"),
            Employee(id="204", ename="Wambli Xolotl", esalary=32000, etitle="sales associate", storeid="002")
        ]
    )
    LosAngeles = Location(
        id="003",
        laddress="789 Los Angeles, CA 90009",
        lphone="2718843621",
        mgrid="301",
        employees=[
            Employee(id="301", ename="Edgardo Stephano", esalary=83000, etitle="manager", storeid="003"),
            Employee(id="302", ename="Serapion Rakel", esalary=39000, etitle="sales associate", storeid="003"),
            Employee(id="303", ename="Anka Sandhya", esalary=24000, etitle="sales associate", storeid="003"),
            Employee(id="304", ename="Manas Felicitas", esalary=19000, etitle="sales associate", storeid="003")
        ]
    )
    Seattle = Location(
        id="004",
        laddress="909 Seattle, WA 98109",
        lphone="9234071938",
        mgrid="401",
        employees=[
            Employee(id="401", ename="Atlas Hasmik", esalary=90000, etitle="manager", storeid="004"),
            Employee(id="402", ename="Ortwin Heraclitus", esalary=47000, etitle="sales associate", storeid="004"),
            Employee(id="403", ename="Yseut Aisopos", esalary=31000, etitle="sales associate", storeid="004"),
            Employee(id="404", ename="Jun Kinich", esalary=44000, etitle="sales associate", storeid="004")
        ]
    )

    session.add_all([Chicago, NewYork, LosAngeles, Seattle])
    session.commit()


class Categories(Base):
    __tablename__ = "Categories"

    cid: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(30))
    brand: Mapped[List["Brand"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # represents the object as a string
        return f"Categories(cid={self.cid!r}, category_name={self.category_name!r})"


class Brand(Base):
    __tablename__ = "Brands"

    bid: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(40))
    cid: Mapped[int] = mapped_column(Integer, ForeignKey("Categories.cid"))
    category: Mapped["Categories"] = relationship(back_populates="brand")

    def __repr__(self) -> str:
        return f"Brand(bid={self.bid!r}, brand_name={self.brand_name!r})"


# Create Tables
Base.metadata.create_all(engine)

# Insert Data
with Session(engine) as session:
    Makeup = Categories(
        category_name="Makeup",
        brand=[Brand(brand_name="Rare Beauty"),
               Brand(brand_name='Kosas'),
               Brand(brand_name='Fenty')],
    )
    SkinCare = Categories(
        category_name="SkinCare",
        brand=[Brand(brand_name="The Ordinary"),
               Brand(brand_name='Drunk Elephant'),
               Brand(brand_name='Glow Recipe')],
    )
    HairCare = Categories(
        category_name="HairCare",
        brand=[Brand(brand_name="Amika"),
               Brand(brand_name='Dry Bar'),
               Brand(brand_name='Olaplex')],
    )
    session.add_all([Makeup, SkinCare, HairCare])
    session.commit()
class Product(Base):
	__tablename__ = 'products'

	pID = Column(String(50), primary_key=True)
	pName = Column(String(100))
	pType = Column(String(100))
	pPrice = Column(Numeric)
	pVariation = Column(String(50))
	bID = Column(String(50), ForeignKey('brands.bID'))
	cID = Column(String(50), ForeignKey('categories.cID'))

	brand = relationship("Brands", back_populates="products")
	category = relationship("Category", back_populates="products")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()products_data = [
	Product(pID='12345', pName='Soft Pinch Liquid', pType='Blush', pPrice=23, pVariation=9, bID='0001', cID='111'),
	Product(pID='23456', pName='Liquid Touch Brightening', pType='Concealer', pPrice=22, pVariation=43, bID='0001',
        	cID='111'),
	Product(pID='73927', pName='Perfect Strokes Volumizing', pType='Mascara', pPrice=20, pVariation=1, bID='0001',
        	cID='111'),
	Product(pID='27369', pName='Kind Words Matte', pType='Lipstick', pPrice=20, pVariation=10, bID='0001', cID='111'),
	Product(pID='24623', pName='Revealer Super Creamy + Brightening', pType='Concealer', pPrice=30, pVariation=38,
        	bID='0002', cID='111'),
	Product(pID='29348', pName='Revealer Skin-Improving Foundation SPF 25 with Hyaluronic Acid and Niacinamide',
        	pType='Foundation', pPrice=42, pVariation=36, bID='0002', cID='111'),
	Product(pID='28362', pName='Big Clean Longwear Volumizing + Lash Care Mascara', pType='Mascara', pPrice=26,
        	pVariation=1, bID='0002', cID='111'),
	Product(pID='67842', pName='Weightless Lip Color Nourishing Satin Lipstick', pType='Lipstick', pPrice=26,
        	pVariation=10, bID='0002', cID='111'),
	Product(pID='23543', pName='Cheeks Out Freestyle Cream Blush', pType='Blush', pPrice=25, pVariation=11, bID='0003',
        	cID='111'),
	Product(pID='96876', pName='Pro Filt’r Soft Matte Longwear Liquid Foundation', pType='Foundation', pPrice=40,
        	pVariation=53, bID='0003', cID='111'),
	Product(pID='48756', pName='Snap Shadows Mix & Match Eyeshadow Palette', pType='Eyeshadow', pPrice=30, pVariation=1,
        	bID='0003', cID='111'),
	Product(pID='35543', pName='Brow MVP Ultra Fine Brow Pencil & Styler', pType='Brow', pPrice=25, pVariation=14,
        	bID='0003', cID='111'),
	Product(pID='98756', pName='Seltzer Spritz Flexible Hold Hairspray', pType='Hairspray', pPrice=31, pVariation=1,
        	bID='0004', cID='333'),
	Product(pID='23565', pName='Liquid Glass Smoothing Shampoo', pType='Shampoo', pPrice=29, pVariation=1, bID='0004',
        	cID='333'),
	Product(pID='75386', pName='Blonde Ale Brightening Conditioner', pType='Conditioner', pPrice=29, pVariation=1,
        	bID='0004', cID='333'),
	Product(pID='34624', pName='Detox Gentle Dry Shampoo Sensitive Scalp', pType='Dry Shampoo', pPrice=28, pVariation=1,
        	bID='0004', cID='333'),
	Product(pID='85765', pName='Glucoside Foaming Cleanser', pType='Face Wash', pPrice=12.5, pVariation=1, bID='0005',
        	cID='222'),
	Product(pID='65234', pName='Natural Moisturizing Factors + HA', pType='Moisturizer', pPrice=14, pVariation=1,
        	bID='0005', cID='222'),
	Product(pID='76476', pName='Hyaluronic Acid 2% + B5 Hydrating Serum', pType='Serum', pPrice=17.5, pVariation=1,
        	bID='0005', cID='222'),
	Product(pID='23587', pName='Niacinamide 10% + Zinc 1% Oil Control Serum', pType='Serum', pPrice=10.8, pVariation=1,
        	bID='0005', cID='222'),
	Product(pID='14345', pName='Beste™ No. 9 Jelly Cleanser', pType='Face Wash', pPrice=34, pVariation=1, bID='0006',
        	cID='222'),
	Product(pID='45673', pName='Lala Retro™ Nourishing Whipped Refillable Moisturizer', pType='Moisturizer', pPrice=62,
        	pVariation=1, bID='0006', cID='222'),
	Product(pID='12543', pName='A-Passioni™ Retinol Cream', pType='Retinol', pPrice=74, pVariation=1, bID='0006',
        	cID='222'),
	Product(pID='54778', pName='B-Hydra™ Intensive Hydration Serum with Hyaluronic Acid', pType='Serum', pPrice=41,
        	pVariation=1, bID='0006', cID='222'),
	Product(pID='23564', pName='No. 4 Bond Maintenance™ Shampoo', pType='Shampoo', pPrice=30, pVariation=1, bID='0007',
        	cID='333'),
	Product(pID='54576', pName='No. 5 Bond Maintenance™ Conditioner', pType='Conditioner', pPrice=30, pVariation=1,
        	bID='0007', cID='333'),
	Product(pID='97753', pName='No. 3 Hair Repair Perfector', pType='Hair Masque', pPrice=60, pVariation=1, bID='0007',
        	cID='333'),
	Product(pID='45319', pName='No. 7 Bonding Hair Oil', pType='Hair Oil', pPrice=30, pVariation=1, bID='0007',
        	cID='333'),
	Product(pID='32654', pName='Top Gloss Hair Shine Spray', pType='Hair Spray', pPrice=29, pVariation=1, bID='0008',
        	cID='333'),
	Product(pID='45457', pName='Normcore Sulfate Free Shampoo', pType='Shampoo', pPrice=38, pVariation=1, bID='0008',
        	cID='333'),
	Product(pID='34654', pName='Perk Up Talc-Free Dry Shampoo', pType='Dry Shampoo', pPrice=28, pVariation=1,
        	bID='0008', cID='333'),
	Product(pID='86954', pName='Soulfood Nourishing Hair Mask', pType='Hair Mask', pPrice=34, pVariation=1, bID='0008',
        	cID='333'),
	Product(pID='45365', pName='Avocado Ceramide Moisture Barrier Cleanser', pType='Face Wash', pPrice=28, pVariation=1,
        	bID='0009', cID='222'),
	Product(pID='32522', pName='Watermelon Pink Juice Oil-Free Refillable Moisturizer', pType='Moisturizer', pPrice=40,
        	pVariation=1, bID='0009', cID='222'),
	Product(pID='77654', pName='Cloudberry Bright Essence Toner', pType='Toner', pPrice=38, pVariation=1, bID='0009',
        	cID='222'),
	Product(pID='54744', pName='Pomegranate Peptide Firming Serum', pType='Serum', pPrice=45, pVariation=1, bID='0009',
        	cID='222')

]
session.add_all(products_data)

session.commit()
class Brands(Base):
	__tablename__ = "brands"

	bID = Column(String(50), primary_key=True)
	bName = Column(String(40))
	bContact = Column(String(30))
	products = relationship("Product", back_populates="brand")

	def __repr__(self) -> str:
    	return f"Brands(id={self.bID!r}, name={self.bName!r}, contact={self.bContact!r})"
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
brands_data = [
	Brands(bID="0001", bName="Rare Beauty", bContact="rarebeautyrep@gmail.com"),
	Brands(bID="0002", bName="Kosas", bContact="kosasrep@gmail.com"),
	Brands(bID="0003", bName="Fenty", bContact="fentyrep@gmail.com"),
	Brands(bID="0004", bName="Dry Bar", bContact="drybarrep@gmail.com"),
	Brands(bID="0005", bName="The Ordinary", bContact="theordinaryrep@gmail.com"),
	Brands(bID="0006", bName="DrunkElephant", bContact="drunkelephantrep@gmail.com"),
	Brands(bID="0007", bName="Olaplex", bContact="olaplexrep@gmail.com"),
	Brands(bID="0008", bName="Amika", bContact="amikarep@gmail.com"),
	Brands(bID="0009", bName="Glow Recipe", bContact="glowreciperep@gmail.com"),

]
session.add_all(brands_data)

session.commit()
class Base(DeclarativeBase):
    pass
class Category(Base):
	 __tablename__ = 'categories'
	cID = Column(String(50), primary_key=True)
	cname = Column(String(100))
	products = relationship("Product", back_populates="category")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

categories_data = [
	Category(cID='111', cname='Makeup'),
	Category(cID='222', cname='Skincare'),
	Category(cID='333', cname='Haircare'),
]
session.add_all(categories_data)

session.commit()

#query 1
managers_at_locations =
(session.query(Location, Employee)
.join(Employee, Location.mgrid == Employee.id))

for location, employee in managers_at_locations:
    print(f"Location Address: {location.laddress}\nManager: {employee.ename}\nManager ID: {location.mgrid}\n")

#query 2
session = Session(engine)
#Join Query
stmt = (
    select(Brand)
    .join(Brand.category)
    .where(Categories.category_name == "Makeup")
)
for brand in session.scalars(stmt):
    print(f'Makeup Brand: brand_name={brand.brand_name}, bid={brand.bid}')

#query 3
cheapest_brand = (
	session.query(Brands.bName, func.round(func.avg(Product.pPrice), 2).label("average_price"))
	.join(Product)
	.group_by(Brands.bName)
	.order_by(func.avg(Product.pPrice))
)

for brand_name, average_price in cheapest_brand:
	print(f"Brand: {brand_name}\nAverage Price: {average_price}\n")

#query 4
CategoryPrice = (
    session.query(Category.cID, Category.cname, func.round(func.sum(Product.pPrice), 2).label("totalprice"))
    .join(Product)
    .group_by(Category.cID, Category.cname)
    .order_by(func.sum(Product.pPrice).desc())
)

for cid, cname, totalprice in CategoryPrice:
    print(f"Category ID: {cid}\nCategory Name: {cname}\nTotal Price: {totalprice}\n")
