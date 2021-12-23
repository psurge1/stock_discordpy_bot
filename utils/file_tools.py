import csv

class csv_tools:
    def __init__(self, default_file_path=None):
        self.file_path = default_file_path
        self.read_return_type = 'ARRAY'

    def __check__(self, path1):
        if path1 != None:
            return path1
        elif self.file_path != None:
            return self.file_path

    def set_read_return_type(self, r_type):
        if r_type in ['ARRAY','STRING','DICTIONARY']:
            self.read_return_type = r_type
        else:
            print("ERROR: return type not supported")

    def read(self, f_path=None):
        rp = self.__check__(f_path)
        if rp == None:
            print("ERROR: no path provided")
            return
        
        with open(rp, 'r') as csvfile:
            return csvfile.read()
    
    def write(self, w_path=None):
        wp = self.__check__(w_path)
        if wp == None:
            print("ERROR: no path provided")
            return
        print("TODO: write()")

class txt_tools:
    def __init__(self, default_file_path=None):
        self.file_path = default_file_path

    def __check__(self, path1):
        if path1 != None:
            return path1
        elif self.file_path != None:
            return self.file_path
    
    def read(self, f_path=None):
        rp = self.__check__(f_path)
        if rp == None:
            print("ERROR: no path provided")
            return
        with open(rp, 'r') as txtfile:
            file_string = txtfile.read()
        return file_string