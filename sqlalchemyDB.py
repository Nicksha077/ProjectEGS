from sqlalchemy import create_engine, ForeignKey, String, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapped_column, relationship
from config import host, user, password, db_name


engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{db_name}", echo=True)


Base = declarative_base()


class Building(Base):
    __tablename__ = 'buildings'
    
    id = mapped_column('id',Integer, primary_key=True)
    street = mapped_column('street', Integer, ForeignKey('streets.id'))
    house = mapped_column('house', String)
    latitude = mapped_column('latitude', Numeric)
    longitude = mapped_column('longitude', Numeric)
    year_construction = mapped_column('year_construction', Integer)
    number_floors = mapped_column('number_floors', Integer)
    number_entrances = mapped_column('number_entrances', Integer)
    number_buildings = mapped_column('number_buildings', Integer)
    number_living_quarters = mapped_column('number_living_quarters', Integer)
    type_construction = mapped_column('type_construction', Integer)
    basic_project = mapped_column('basic_project', Integer)
    appointment = mapped_column('appointment', Integer)
    seismic_resistance_min = mapped_column('seismic_resistance_min', Numeric)
    seismic_resistance_max = mapped_column('seismic_resistance_max', Numeric)
    seismic_resistance_soft = mapped_column('seismic_resistance_soft', String)
    zone_smz_min = mapped_column('zone_smz_min', Numeric)
    zone_smz_max = mapped_column('zone_smz_max', Numeric)
    zone_smz_increment = mapped_column('zone_SMZ_increment', Numeric)
    wear_rate = mapped_column('wear_rate', Numeric)
    priming = mapped_column('priming', Integer)
    load_bearing_walls = mapped_column('load_bearing_walls', Numeric)
    basement_area = mapped_column('basement_area', Numeric)
    building_roof = mapped_column('building_roof', Integer)
    building_floor = mapped_column('building_floor', Integer)
    facade = mapped_column('facade', Integer),
    foundation = mapped_column('foundation', Integer)
    cadastral_cost = mapped_column('cadastral_cost', Numeric)
    
    street_obj = relationship("Street", back_populates="buildings")
    
# Определение модели Street
class Street(Base):
    __tablename__ = 'streets'
    
    id = mapped_column('id', Integer, primary_key=True)
    name = mapped_column('name', String)
    
    buildings = relationship("Building", back_populates="street_obj")
    
# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()




def request_to_DB():
# Запрос к базе данных
    return session.query(Building.id, Street.name, Building.house, Building.latitude, Building.longitude, 
                            Building.seismic_resistance_soft, Building.zone_smz_min, Building.zone_smz_max, 
                            Building.cadastral_cost, Building.year_construction, Building.seismic_resistance_min, 
                            Building.seismic_resistance_max)\
                        .join(Street, Building.street==Street.id)\
                        .filter(Building.cadastral_cost != None)\
                        .filter(Building.seismic_resistance_soft != None)\
                        .all()

# Вывод результатов
# for b in buildings:
#     print(b)