import os
from popups import display_message
from openpyxl import load_workbook
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
            wb = load_workbook(filename = 'template.xlsx')
            ws = wb.active
            for id_number in self.id_numbers:
                ws[f"C{count}"] = id_number
                count += 1
            wb.save(filename = destination)
            print(destination)
            display_message(1, file_name=file_name, path=self.directory)
        except Exception as e:
            display_message(repr(e))