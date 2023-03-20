import PySimpleGUI as sg

# Protoype window layout template for ReservationsSystem
class stubWindow:
    def __init__(self, theme='lightGreen'):
        
        self._themeStr = theme
        self._gender = ""
        self._destinations = []
        
        # Set GUI theme           
        sg.theme(self._themeStr)

        self._layout = [self._getFormLayout(), self._getButtonLayout()]

        self._window = sg.Window('Stub Window', self._layout, keep_on_top=True, finalize=False)


    def _getFormLayout(self) -> list:
		# Retrieval of screen values goes here
        self._destinations = ['New York', 'London', 'Tokyo', 'Madrid', 'Paris', 'Brussels']
        
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
    
    def _clearEntries(self) -> None:
        self._window['-Name-'].update(value="")
        self._window['-Passport_Number-'].update(value="")
        self._window['-Male-'].update(value=False)
        self._window['-Female-'].update(value=False)
        self._window['-Departure-'].update(value="")
        self._window['-Arrival-'].update(value="")
        self._window['-Destination-'].update(set_to_index=[])
        self._window['-Name-'].set_focus(force=True)
        
        
    def run(self) -> None:
		# Process events
        while True:      
            event, values = self._window.Read() 
            print(event, values)
            if event in ('Exit', sg.WIN_CLOSED):
                break
            elif event == 'Reserve Ticket':
				# Validation processing goes here
				# Database persistence goes here
                self._clearEntries()  # Clear screen after successful db CREATE
                continue
            elif event == 'See Reservations':
				# Display new screen here
                continue
            else:
                continue

        self._window.close()
        
        
def main():
    
    App = stubWindow('DarkAmber')
    App.run()


if __name__ == '__main__':
	main()
