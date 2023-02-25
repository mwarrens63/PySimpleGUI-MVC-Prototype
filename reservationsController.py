# Connects reservationsView with reservationsModel.
# Provides high-level CRUD methods connecting reservationsView to reservationsModel.
# Converts reservationsModel data to a format usable by reservationsView.
# Updates reservationsView when the reservationsModel has changed.

from PySimpleGUI import TreeData
import reservationsModel as rm


# Converts dict returned by getReservationsData() to
# list of lists: each list is a row in the Reservations table	
def _retrieveReservationsList() -> list:
	tableData = rm.getReservationsData()
	valuesList = [*[list(idx.values()) for idx in tableData ]]
	return(valuesList)


# Converts dict returned by getDestinationsData() to
# list of lists: each list is a row in the Destinations table
def _retrieveDestinationsList() -> list:
	tableData = rm.getDestinationsData()
	valuesList = [*[list(idx.values()) for idx in tableData ]]
	return(valuesList)

    
def retrieveTreeColumnNames() -> list:
    columnNames = rm.retrieveColumnNames()
    return(columnNames)


# PySimpleGUI.TreeData
def _retrieveTreeData() -> TreeData:
    treedata = TreeData()
    
    reservationsList = _retrieveReservationsList()

    # Convert to PySimpleGUI TreeData format
    n = 0
    for res in reservationsList:
        n += 1
        keystr = "-row_{}-".format(n)
        treedata.Insert('', key=keystr, text= n, values=res)
        
    return(treedata)


def retrieveReservations() -> TreeData:
    treedata = _retrieveTreeData()
    return(treedata)
            
            
def retrieveDestinations() -> list:
    destinations = _retrieveDestinationsList()
    return(destinations)


def deleteReservation(idval, viewRef=None) -> None:
    rm.deleteReservation(idval)
    # Update Reservations Window Tree
    if viewRef != None:
        viewRef.treedata = _retrieveTreeData()
        viewRef.refreshTree()
    return()


def createReservation(name, gender, passport_num, destination, departure_dt, arrival_dt) -> None:
    rm.createReservation(name, gender, passport_num, destination, departure_dt, arrival_dt)
    return()


def updateReservation(idVal, name, gender, passport_num, destination, departure_dt, arrival_dt, viewRef=None) -> None:
    rm.updateReservation(idVal, name, gender, passport_num, destination, departure_dt, arrival_dt)
    # Update Reservations Window Tree
    if viewRef != None:
        viewRef.treedata = _retrieveTreeData()
        viewRef.refreshTree()
    return()


# For tesing   
def main():
    
    lst = retrieveTreeColumnNames()
    print("Column Names: ", lst)
    print()
    TreeData = _retrieveTreeData()
    print(TreeData)
    # createReservation('Robert Warren', 'Male', 'M897645', 'Tokyo', '2022-10-20 21:07:54', '2022-10-21 21:07:57')
    

if __name__ == '__main__':
	main()