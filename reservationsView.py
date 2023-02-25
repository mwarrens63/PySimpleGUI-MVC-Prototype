# Provides the GUI for the "Flight Reservations System" via PySimpleGUI.
# Connects to the reservationsModel module via the reservationsController module.
# Validates user input before sending data to the reservationsModel via the reservationsController.
# Where necessary, the reservationsView passes references to GUI windows so that the reservationsController
# can update the reservationsView.

import PySimpleGUI as sg
import reservationsController as rc
from datetime import datetime


# Window for creating reservations
class ReservationsSystem:
    def __init__(self, theme='lightGreen'):
        
        self._themeStr = theme
        self._gender = ""
        self._destinations = []
        
        # Set GUI theme           
        sg.theme(self._themeStr)

        self._layout = [self._getFormLayout(), self._getButtonLayout()]

        self._window = sg.Window('Flight Reservations System', self._layout, keep_on_top=True, finalize=False)


    def _getFormLayout(self) -> list:
        self._destinations = rc.retrieveDestinations()# RETRIEVE Destinations for ListBox
        
        layout = [
            [sg.Text("Full name:"), sg.Input(key='-Name-', do_not_clear=True, size=(20,1))],
            [sg.Text("Passport number:"), sg.Input(key='-Passport_Number-', do_not_clear=True, size=(10,1))],
            [sg.Radio("Male", "RADIO", key='-Male-'), sg.Radio("Female", 'RADIO', key='-Female-')],
            [sg.Input(key='-Departure-', size=(20,1)), sg.CalendarButton("Date of Departure", close_when_date_chosen=True, target='-Departure-', no_titlebar=False)],
            [sg.Input(key='-Arrival-', size=(20,1)), sg.CalendarButton("Date of Arrival", close_when_date_chosen=True, target='-Arrival-', no_titlebar=False)],
            [sg.Text("Select A Destination:")],
            [sg.Listbox(values=self._destinations, key='-Destination-', size=(40,5), select_mode="single")]
        ]
        return(layout)
    
    
    def _getButtonLayout(self) -> list:
        layout = [
            [sg.Button("Reserve Ticket"), sg.Button('See Reservations'), sg.Exit()]
        ]
        return(layout)

        
    # Get radio button value and set gender
    def _setGender(self, values: dict) -> str:
        gender = ""
        if values['-Male-']: # bool
            gender = 'Male'
        else:
            gender = 'Female'
        return(gender)
            

    def _formatReservationInfo(self, values: dict) -> str: 
        tdest = values['-Destination-'][0][0]
        msg = "Reservation for \nName: {} \nGender: {}\nPassport #: {}\nDestination: {}\nDeparture: {}\nArrival: {} \nsaved."\
            .format(values['-Name-'], self._gender,  values['-Passport_Number-'], tdest, values['-Departure-'], values['-Arrival-'])
        
        return(msg)
    
    # Add reservations to reservations.db
    def _saveReservation(self, values: dict) -> None:
        tdest = values['-Destination-'][0][0]
        # CREATE reservation
        rc.createReservation(values['-Name-'], self._gender,  values['-Passport_Number-'], tdest, values['-Departure-'], \
            values['-Arrival-'])
        
        
    def _clearEntries(self) -> None:
        self._window['-Name-'].update(value="")
        self._window['-Passport_Number-'].update(value="")
        self._window['-Male-'].update(value=False)
        self._window['-Female-'].update(value=False)
        self._window['-Departure-'].update(value="")
        self._window['-Arrival-'].update(value="")
        self._window['-Destination-'].update(set_to_index=[])
        self._window['-Name-'].set_focus(force=True)
    
    
    def _is_arrival_before_departure(self, values: dict) -> bool:
        departure_obj = datetime.strptime(values['-Departure-'], "%Y-%m-%d %H:%M:%S")
        arrival_obj = datetime.strptime(values['-Arrival-'], "%Y-%m-%d %H:%M:%S")
        
        if arrival_obj > departure_obj:
            return (False)
        
        return(True)
    
    
    def _is_departure_before_now(self, values: dict) -> bool:
        departure_obj = datetime.strptime(values['-Departure-'], "%Y-%m-%d %H:%M:%S")
        now_obj = datetime.now()
        
        if departure_obj > now_obj:
            return(False)
        
        return(True)
    
    
    def _is_arrival_before_now(self, values: dict) -> bool:
        arrival_obj = datetime.strptime(values['-Arrival-'], "%Y-%m-%d %H:%M:%S")
        now_obj = datetime.now()
        
        if arrival_obj > now_obj:
            return(False)
        
        return(True)
    
    
    def _validate(self, values: dict) -> tuple[bool, str]:
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
            if self._is_departure_before_now(values):
                values_invalid.append('Departure Date comes before today\'s date!!!\n')
                is_valid = False 
                
                
        if len(values['-Arrival-']) == 0:
            values_missing.append('Arrival Date')
            is_valid = False 
            
            
        if len(values['-Arrival-']) > 0:
            if self._is_arrival_before_now(values):
                values_invalid.append('Arrival Date comes before today\'s date!!!\n')
                is_valid = False 
                   
            
        if len(values['-Departure-']) > 0 and len(values['-Arrival-']) > 0:
            if self._is_arrival_before_departure(values):
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
            event, values = self._window.Read() 
            
            if event in ('Exit', sg.WIN_CLOSED):
                break
            elif event == 'Reserve Ticket':
                self._gender = self._setGender(values)
                
                is_valid, error_msg = self._validate(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                
                # Save reservation to db
                self._saveReservation(values)
                
                msg = self._formatReservationInfo(values)    
                sg.popup("Ticket Reserved", msg, keep_on_top=True)
                
                self._clearEntries()
                continue
            elif event == 'See Reservations':
                # Instantiate and display modal Reservations Window
                resWin = ReservationsWindow("Reservations", theme=self._themeStr)
                resWin.run()
                continue
        
        self._window.close()



# Modal window for diplaying and deleting reservations
class ReservationsWindow:
    def __init__(self, title, theme='lightGreen') -> None:
        self._themeStr = theme
        sg.theme(self._themeStr)
        self._title = title
        
        self.treedata = sg.TreeData() # Used by reservationsController
        
        _treeLayout = self._getTreeLayout()
        _buttonLayout= [sg.Button('Delete Reservation', disabled=True), sg.Button('Edit Reservation', disabled=True), sg.Exit()]
        
        _layout = [_treeLayout, _buttonLayout]
        
        self._window = sg.Window(self._title, _layout, modal=True, keep_on_top=True, finalize=True)


    def _getTreeLayout(self) -> list:
        
        self.treedata = rc.retrieveReservations() # RETRIEVE reservations from database
        columns = rc.retrieveTreeColumnNames() # RETRIEVE table column verbose names from database

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
        
    
    # Used by reservationsController to update View
    def refreshTree(self) -> None:
        self._window['-TREE-'].update(values=self.treedata)
        # print("executed refreshTree()")
        return()
        
    
    def _disableDeleteButton(self, val: bool) -> None:
        self._window['Delete Reservation'].update(disabled=val)
        return()
    
    
    def _disableEditButton(self, val: bool) -> None:
        self._window['Edit Reservation'].update(disabled=val)
        return()
        
        
    def run(self) -> None:
        # Process events
        while True:
            event, values = self._window.Read() 

            if event in ('Exit', sg.WIN_CLOSED):
                break 
            elif event in ('-TREE-'):  # Tree row selected
                try: 
                    selected_row_key = values['-TREE-'][0] # This is key for the selected row
                    rowdata = self._window.Element('-TREE-').TreeData.tree_dict[selected_row_key].values
                    self._disableDeleteButton(False)
                    self._disableEditButton(False)
                    continue
                except IndexError: # Ignore this exception (occurs when the tree is refreshed)
                    continue
            elif event in ('Delete Reservation'):
                # DELETE selected reservation using reservation_id; refrence to self enables controller to refreshTree()
                rc.deleteReservation(rowdata[0], self) 
                self._disableDeleteButton(True)
                self._disableEditButton(True)
                continue
            # Display Edit Reservation Window: pass reference to self
            elif event in ('Edit Reservation'):
                editWin = ReservationsEditWindow(self, rowdata, 'DarkAmber') 
                editWin.run()
                continue
                
        self._window.close()


        
# Modal Window for editing reservations, note use of inheritance     
class ReservationsEditWindow(ReservationsSystem):  
    def __init__(self, resWin, rowdata, theme='lightGreen'):
        self._resWin = resWin # Parent Reservations Window
        self._rowdata = rowdata
        self._themeStr = theme
        self._gender = ""
        
        # Set GUI theme           
        sg.theme(self._themeStr)

        self._layout = [self._getIdLayout(), super()._getFormLayout(), self._getButtonLayout()]
        self._window = sg.Window('Edit Reservation', self._layout, modal=True, keep_on_top=True, finalize=True)
        
        self.populateEntries(self._rowdata, self._window)
        
        
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
            
        destList = [str(e[0]) for e in self._destinations] # Get list of destinations strings
        index = destList.index(rowdata[4])
        window['-Destination-'].update(set_to_index=[index])
        
        date_time = rowdata[5].strftime("%Y-%m-%d %H:%M:%S") 
        window['-Departure-'].update(value=date_time)
        
        date_time = rowdata[6].strftime("%Y-%m-%d %H:%M:%S")
        window['-Arrival-'].update(value=date_time)
        
        window['-Name-'].set_focus(force=True)
         
        
    def _getIdLayout(self) -> list:
          layout = [sg.Text("Id:"), sg.Input(key='-Id-', do_not_clear=True, readonly=True, \
              disabled_readonly_background_color = 'gray', size=(5,1))]
          return(layout)
      
    # Override this method to change button label
    def _getButtonLayout(self) -> list:
        layout = [
            [sg.Button('Save Reservation'), sg.Exit()]
        ]
        return(layout)
    
    
    def _saveReservation(self, values: dict) -> tuple[bool,str]:
        tdest = values['-Destination-'][0][0]
        # Update reservation
        try:
            # Pass refrence to resWin to enable controller to execute resWin.refreshTree()
            rc.updateReservation(values['-Id-'], values['-Name-'], self._gender,  values['-Passport_Number-'], \
                tdest, values['-Departure-'], values['-Arrival-'], self._resWin)
            retval = (True, "Update successful")
            return(retval)
        except Exception as e:
            retval = (False, e)
            return(retval)
    
    
    def run(self) -> None:
        # Process events
        while True:      
            event, values = self._window.Read() 
            
            if event in (sg.WIN_CLOSED, 'Exit'):      
                break
            elif event == 'Save Reservation':
                self._gender = super()._setGender(values)

                is_valid, error_msg = super()._validate(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                
                # Update reservation
                is_valid, error_msg = self._saveReservation(values)
                if (not is_valid):
                    sg.popup("Error", error_msg, keep_on_top=True)
                    continue
                else:
                    sg.popup("Success", "Edit Saved", keep_on_top=True)
                
                continue
        
        self._window.close()
    

    
def main():
    
    App = ReservationsSystem('DarkAmber')
    App.run()


if __name__ == '__main__':
	main()
