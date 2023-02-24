# Connects reservationsView with reservationsModel.
# Provides high-level CRUD methods connecting reservationsView to reservationsModel.
# Updates reservationsView when the reservationsModel has changed.

from PySimpleGUI import TreeData
import reservationsModel as rm

    
def retrieveTreeColumnNames() -> list:
    columnNames = rm.retrieveColumnNames()
    return(columnNames)


# PySimpleGUI.TreeData
def _retrieveTreeData() -> TreeData:
    treedata = TreeData()
    
    reservationsList = rm.retrieveReservations() # RETRIEVE reservations from database

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
    destinations = rm.retrieveDestinations()
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
        viewRef.treedata = retrieveTreeData()
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