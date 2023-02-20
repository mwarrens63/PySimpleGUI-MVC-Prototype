# Provides the GUI for the "Flight Reservations System" via PySimpleGUI.
# Connects to the reservationsModel module via the reservationsController module.
# Validates user input before sending data to the reservationsModel via the reservationsController.
# Where necessary, the reservationsView passes references to GUI windows so that the reservationsController
# can update the reservationsView.

import PySimpleGUI as sg
import reservationsController
from datetime import datetime


# Window for creating reservations
class ReservationsSystem:
    def __init__(self, theme='lightGreen'):
        
        self.themeStr = theme
        self.gender = ""
        self.destinations = []
        
        # Set GUI theme           
        sg.theme(self.themeStr)

        self.layout = [self.getFormLayout(), self.getButtonLayout()]

        self.window = sg.Window('Flight Reservations System', self.layout, keep_on_top=True, finalize=False)


    def getFormLayout(self) -> list:
        self.destinations = reservationsController.retrieveDestinations()# RETRIEVE Destinations for ListBox
        
        layout = [
            [sg.Text("Full name:"), sg.Input(key='-Name-', do_not_clear=True, size=(20,1))],
            [sg.Text("Passport number:"), sg.Input(key='-Passport_Number-', do_not_clear=True, size=(10,1))],
            [sg.Radio("Male", "RADIO", key='-Male-'), sg.Radio("Female", 'RADIO', key='-Female-')],
            [sg.Input(key='-Departure-', size=(20,1)), sg.CalendarButton("Date of Departure", close_when_date_chosen=True, target='-Departure-', no_titlebar=False)],
            [sg.Input(key='-Arrival-', size=(20,1)), sg.CalendarButton("Date of Arrival", close_when_date_chosen=True, target='-Arrival-', no_titlebar=False)],
            [sg.Text("Select A Destination:")],
            [sg.Listbox(values=self.destinations, key='-Destination-', size=(40,5), select_mode="single")]
        ]
        return(layout)
    
    
    def getButtonLayout(self) -> list:
        layout = [
            [sg.Button("Reserve Ticket"), sg.Button('See Reservations'), sg.Exit()]
        ]
        return(layout)

        
    # Get radio button value and set gender
    def setGender(self, values: dict) -> str:
        gender = ""
        if values['-Male-']: # bool
            gender = 'Male'
        else:
            gender = 'Female'
        return(gender)
            

    def formatReservationInfo(self, values: dict) -> str: 
        tdest = values['-Destination-'][0][0]
        msg = "Reservation for \nName: {} \nGender: {}\nPassport #: {}\nDestination: {}\nDeparture: {}\nArrival: {} \nsaved."\
            .format(values['-Name-'], self.gender,  values['-Passport_Number-'], tdest, values['-Departure-'], values['-Arrival-'])
        
        return(msg)
    
    # Add reservations to reservations.db
    def saveReservation(self, values: dict) -> None:
        tdest = values['-Destination-'][0][0]
        # CREATE reservation
        reservationsController.createReservation(values['-Name-'], self.gender,  values['-Passport_Number-'], tdest, values['-Departure-'], \
            values['-Arrival-'])
        
        
    def clearEntries(self) -> None:
        self.window['-Name-'].update(value="")
        self.window['-Passport_Number-'].update(value="")
        self.window['-Male-'].update(value=False)
        self.window['-Female-'].update(value=False)
        self.window['-Departure-'].update(value="")
        self.window['-Arrival-'].update(value="")
        self.window['-Destination-'].update(set_to_index=[])
        self.window['-Name-'].set_focus(force=True)
    
    
    def is_arrival_before_departure(self, values: dict) -> bool:
        departure_obj = datetime.strptime(values['-Departure-'], "%Y-%m-%d %H:%M:%S")
        arrival_obj = datetime.strptime(values['-Arrival-'], "%Y-%m-%d %H:%M:%S")
        
        if arrival_obj > departure_obj:
            return (False)
        
        return(True)
    
    
    def is_departure_before_now(self, values: dict) -> bool:
        departure_obj = datetime.strptime(values['-Departure-'], "%Y-%m-%d %H:%M:%S")
        now_obj = datetime.now()
        
        if departure_obj > now_obj:
            return(False)
        
        return(True)
    
    
    def is_arrival_before_now(self, values: dict) -> bool:
        arrival_obj = datetime.strptime(values['-Arrival-'], "%Y-%m-%d %H:%M:%S")
        now_obj = datetime.now()
        
        if arrival_obj > now_obj:
            return(False)
        
        return(True)
    
    
    def validate(self, values: dict) -> tuple[bool, str]:
        is_valid = True
        values_invalid = []
        values_missing = []
        
        if len(values['-Name-']) == 0:
            values_missing.append('Name')
            is_valid = False
            
        if len(values['-Passport_Number-']) == 0:
            values_missing.append('Passport Number')
            is_valid = False
            
        if not values['-Male-'] and not values['-Female-']:
            values_missing.append("Gender")
            is_valid = False
            
        if len(values['-Departure-']) == 0:
            values_missing.append('Departure Date')
            is_valid = False 
            
            
        if len(values['-Departure-']) > 0:
            if self.is_departure_before_now(values):
                values_invalid.append('Departure Date comes before today\'s date!!!\n')
                is_valid = False 
                
                
        if len(values['-Arrival-']) == 0:
            values_missing.append('Arrival Date')
            is_valid = False 
            
            
        if len(values['-Arrival-']) > 0:
            if self.is_arrival_before_now(values):
                values_invalid.append('Arrival Date comes before today\'s date!!!\n')
                is_valid = False 
                   
            
        if len(values['-Departure-']) > 0 and len(values['-Arrival-']) > 0:
            if self.is_arrival_before_departure(values):
                values_invalid.append('Arrival Date comes before Departure Date!')
                is_valid = False 
            
        try:  # ListBox validation
            values['-Destination-'][0][0]
        except IndexError:
            values_missing.append('Destination')
            is_valid = False
            
        missingMsg = "Missing data for the following fields: " + "\n" + ",\n".join(values_missing)
        invalidMsg = "".join(values_invalid)
        errorMsg = missingMsg + "\n" + "\nDate/Time Errors:\n" + invalidMsg
            
        result = (is_valid, errorMsg)  
            
        return(result)
        

    def run(self) -> None:
        # Process events
        while True:      
            event, values = self.window.Read() 
            
            if event in ('Exit', sg.WIN_CLOSED):
                break
            elif event == 'Reserve Ticket':
                self.gender = self.setGender(values)
                
                is_valid, error_msg = self.validate(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                
                # Save reservation to db
                self.saveReservation(values)
                
                msg = self.formatReservationInfo(values)    
                sg.popup("Ticket Reserved", msg, keep_on_top=True)
                
                self.clearEntries()
                continue
            elif event == 'See Reservations':
                # Instantiate and display modal Reservations Window
                resWin = ReservationsWindow("Reservations", theme=self.themeStr)
                resWin.run()
                continue
        
        self.window.close()



# Modal window for diplaying and deleting reservations
class ReservationsWindow:
    def __init__(self, title, theme='lightGreen') -> None:
        self.themeStr = theme
        sg.theme(self.themeStr)
        self.title = title
        self.treedata = sg.TreeData()
        
        treeLayout = self.getTreeLayout()
        buttonLayout= [sg.Button('Delete Reservation', disabled=True), sg.Button('Edit Reservation', disabled=True), sg.Exit()]
        
        layout = [treeLayout, buttonLayout]
        
        self.window = sg.Window(self.title, layout, modal=True, keep_on_top=True, finalize=True)


    def getTreeLayout(self) -> list:
        
        self.treedata = reservationsController.retrieveTreeData() # RETRIEVE reservations from database
        columns = reservationsController.retrieveTreeColumnNames() # RETRIEVE table column verbose names from database

        # Tree Frame Layout
        treeLayout = [
            [sg.Tree(data=self.treedata,
                col0_heading='Row',
                headings=columns,
                auto_size_columns=True,
                justification = 'left',
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,  # Single row selection
                num_rows=20,
                col0_width=5,
                key='-TREE-',
                show_expanded=False,
                enable_events=True,
                expand_x=True,
                expand_y=True,
                    )]
        ]
        return(treeLayout)
        
    
    def refreshTree(self) -> None:
        self.window['-TREE-'].update(values=self.treedata)
        # print("executed refreshTree()")
        return()
        
    
    def disableDeleteButton(self, val: bool) -> None:
        self.window['Delete Reservation'].update(disabled=val)
        return()
    
    
    def disableEditButton(self, val: bool) -> None:
        self.window['Edit Reservation'].update(disabled=val)
        return()
        
        
    def run(self) -> None:
        # Process events
        while True:
            event, values = self.window.Read() 

            if event in ('Exit', sg.WIN_CLOSED):
                break 
            elif event in ('-TREE-'):  # Tree row selected
                try: 
                    selected_row_key = values['-TREE-'][0] # This is key for the selected row
                    rowdata = self.window.Element('-TREE-').TreeData.tree_dict[selected_row_key].values
                    self.disableDeleteButton(False)
                    self.disableEditButton(False)
                    continue
                except IndexError: # Ignore this exception when the tree is refreshed
                    continue
            elif event in ('Delete Reservation'):
                # DELETE selected reservation using reservation_id; refrence to self enables controller to refreshTree()
                reservationsController.deleteReservation(rowdata[0], self) 
                self.disableDeleteButton(True)
                self.disableEditButton(True)
                continue
            # Display Edit Reservation Window: pass reference to self
            elif event in ('Edit Reservation'):
                editWin = ReservationsEditWindow(self, rowdata, 'DarkAmber') 
                editWin.run()
                continue
                
        self.window.close()


        
# Modal Window for editing reservations, note use of inheritance     
class ReservationsEditWindow(ReservationsSystem):  
    def __init__(self, resWin, rowdata, theme='lightGreen'):
        self.resWin = resWin # Parent Reservations Window
        self.rowdata = rowdata
        self.themeStr = theme
        self.gender = ""
        
        # Set GUI theme           
        sg.theme(self.themeStr)

        self.layout = [self.getIdLayout(), super().getFormLayout(), self.getButtonLayout()]
        self.window = sg.Window('Edit Reservation', self.layout, modal=True, keep_on_top=True, finalize=True)
        
        self.populateEntries(self.rowdata, self.window)
        
        
    def populateEntries(self, rowdata: list, window: sg.Window) -> None:
        window['-Id-'].update(value=rowdata[0])
        window['-Name-'].update(value=rowdata[1])
        window['-Passport_Number-'].update(value=rowdata[3])
        
        if rowdata[2] == 'Male':
            window['-Male-'].update(value=True)
            window['-Female-'].update(value=False)
        else:
            window['-Male-'].update(value=False)
            window['-Female-'].update(value=True)
            
        destList = [str(e[0]) for e in self.destinations] # Get list of destinations strings
        index = destList.index(rowdata[4])
        window['-Destination-'].update(set_to_index=[index])
        
        date_time = rowdata[5].strftime("%Y-%m-%d %H:%M:%S") 
        window['-Departure-'].update(value=date_time)
        
        date_time = rowdata[6].strftime("%Y-%m-%d %H:%M:%S")
        window['-Arrival-'].update(value=date_time)
        
        window['-Name-'].set_focus(force=True)
         
        
    def getIdLayout(self) -> list:
          layout = [sg.Text("Id:"), sg.Input(key='-Id-', do_not_clear=True, readonly=True, \
              disabled_readonly_background_color = 'gray', size=(5,1))]
          return(layout)
      
      
    def getButtonLayout(self) -> list:
        layout = [
            [sg.Button('Save Reservation'), sg.Exit()]
        ]
        return(layout)
    
    
    def saveReservation(self, values: dict) -> tuple[bool,str]:
        tdest = values['-Destination-'][0][0]
        # Update reservation
        try:
            # Pass refrence to resWin to enable controller to execute resWin.refreshTree()
            reservationsController.updateReservation(values['-Id-'], values['-Name-'], self.gender,  values['-Passport_Number-'], \
                tdest, values['-Departure-'], values['-Arrival-'], self.resWin)
            retval = (True, "Update successful")
            return(retval)
        except Exception as e:
            retval = (False, e)
            return(retval)
    
    
    def run(self) -> None:
        # Process events
        while True:      
            event, values = self.window.Read() 
            
            if event in (sg.WIN_CLOSED, 'Exit'):      
                break
            elif event == 'Save Reservation':
                self.gender = super().setGender(values)

                is_valid, error_msg = super().validate(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                
                # Update reservation
                is_valid, error_msg = self.saveReservation(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                else:
                    sg.popup("Success", "Edit Saved", keep_on_top=True)
                
                continue
        
        self.window.close()
    

    
def main():
    
    App = ReservationsSystem('DarkAmber')
    App.run()


if __name__ == '__main__':
	main()
