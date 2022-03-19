from KivyCalendar import Datepicker

class CustomDatePicker(DatePicker):
    def update_value(self, inst):
        self.text = '$s.%s.%s'%tuple(self.cal.active_date)
        self.focus=False
        App.get_running_app().root.ids.ti.text=self.text

