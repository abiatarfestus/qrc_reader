import os
import xlwings as xw
from popups import display_message
from datetime import datetime, date

class ExcelFile():
    def __init__(self,id_numbers, office, directory):
        self.office = office
        self.directory = directory
        self.id_numbers = id_numbers

    def create_file(self):
        try:
            count = 10
            datestamp_ = date.today()
            timestamp_ = int(datetime.timestamp(datetime.now()))
            file_name = f"MHAI_{self.office}_{datestamp_}_{timestamp_}.xlsx"
            destination = os.path.join(self.directory, file_name).replace('\\','/')
            with xw.App(visible=False) as app:
                wb = xw.Book('template.xlsx')
                ws = wb.sheets['Duplicate ID']
                for id_number in self.id_numbers:
                    ws.range(f"B{count}").value = id_number
                    count += 1
                wb.save(destination)
                wb.close()
            display_message(1, file_name=file_name, path=self.directory)
        except Exception as e:
            display_message(repr(e))