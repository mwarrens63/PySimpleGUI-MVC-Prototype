# Uses the peewee ORM classes/methods to create and manage Sqlite tables for reservation.db
# Provides low level CRUD methods for reservations.db

from peewee import *

# ORM Classes and methods to manage corresponding Sqlite tables for reservations.db --------------------------------------------------------------
db = SqliteDatabase("reservations.db")

class BaseModel(Model):
    class Meta:
        database = db


class Reservations(BaseModel):
    reservation_id = AutoField(primary_key = True, verbose_name = 'Reservation Id') 
    name = CharField(null = False, verbose_name='Name')
    gender = CharField(null = False, verbose_name='Gender')
    passport_number = CharField(null = False, verbose_name = 'Passport #')
    destination = CharField(null = False, verbose_name='Destination')
    departure_dt = DateTimeField(null = False, verbose_name = 'Departure Date/Time')
    arrival_dt = DateTimeField(null = False, verbose_name = 'Arrival Date/Time')


class Destinations(BaseModel):
    destination_id = AutoField(primary_key = True, verbose_name = 'Destination Id')
    city = CharField(null = False, verbose_name='City')
    country = CharField(null = True, verbose_name='Country')
    
    
def create_tables():
    db.connect()
    db.create_tables([Reservations, Destinations])
    db.close()
    
    
def drop_Destinations_table():
    db.connect()
    db.drop_tables([Destinations])
    db.close()
    print("Dropped Destinations table.")
    

def create_Destinations_table():
    db.connect()
    db.create_tables([Destinations])
    db.close()
    print("Created Destinations table.")
    
    
def addDestinationsRecords():
	cities = ['Havana','Moscow','Beijing', 'London', 'Tokyo', 'Paris', 'Tehran', 'Damascus', '\
     Sanaa', 'Tripoli', 'Jerusalem']
	for item in cities:
		Destinations.create(city=item)
	db.commit
	print("Added Destinations records.")
 

def drop_tables():
    db.connect()
    db.drop_tables([Reservations, Destinations])
    db.close()
    

def list_tables():
    db.connect()
    print('reservations.db persistence tables: ', db.get_tables())
    db.close()


# Creates sqlite db tables corresponding to peewee model classes
def createReservationsTables():
	
	db = SqliteDatabase("reservations.db")
	db.connect()

	tables = ''
	tables = db.get_tables()

	list_tables()

	print()
	print("You must drop existing tables before creating new ones.")
	print()

	if (tables != ''):
		response = input('Drop existing reservations tables? (y/n): ')
		if (response == 'y'):
			print('Dropping reservations tables')
			drop_tables()
		else:
			db.close()
			exit()

	print("Creating reservations db tables")
	print()
	create_tables()

	print("Created the following tables:")
	print()
	list_tables()

	db.close()
# Endo of ORM Classes and methods to manage corresponding Sqlite tables -------------------------------------------------------------- 


# CRUD methods -----------------------------------------------------------------------------------------------------------------------
def getReservationsData() -> dict:
	tableData = Reservations.select().order_by(Reservations.reservation_id.desc()).dicts()
	return(tableData)


def getDestinationsData() -> dict:
    tableData = Destinations.select(Destinations.city).order_by(Destinations.city.asc()).dicts()
    return(tableData)
	
	
def retrieveColumnNames() -> list:
	fieldNames = [
        Reservations.reservation_id.verbose_name,
        Reservations.name.verbose_name,
        Reservations.gender.verbose_name,
        Reservations.passport_number.verbose_name,
        Reservations.destination.verbose_name,
        Reservations.departure_dt.verbose_name,
        Reservations.arrival_dt.verbose_name             
]
	return(fieldNames)

	
def deleteReservation(idval) -> None:
	record = Reservations.get(Reservations.reservation_id == idval)
	record.delete_instance()
	db.commit
	
 
def createReservation(name, gender, passport_num, destination, departure_dt, arrival_dt) -> None:
	Reservations.create(name=name, gender=gender, passport_number=passport_num, destination=destination, departure_dt=departure_dt, \
     arrival_dt=arrival_dt)
	db.commit
 
 
def updateReservation(idVal, name, gender, passport_num, destination, departure_dt, arrival_dt) -> None:
    record = Reservations.select().where(Reservations.reservation_id == idVal).get()
    record.name = name
    record.gender = gender
    record.passport_number = passport_num
    record.destination = destination
    record.departure_dt = departure_dt
    record.arrival_dt = arrival_dt
    record.save()
    db.commit
    
# End of CRUD methods -----------------------------------------------------------------------------------------------------------------------


# Drop/Create/Load tables
# Test CRUD methods
def main():

	# drop_Destinations_table()
	# create_Destinations_table()
	# addDestinationsRecords()
    # createReservation('Robert Warren', 'Male', 'M897645', None, '2022-10-20 21:07:54', '2022-10-21 21:07:57')
    tableData = getReservationsData()
    print(*tableData)

 
if __name__ == '__main__':
    main()