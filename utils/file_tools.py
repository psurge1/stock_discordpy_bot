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
        if r_type in ['ARRAY','STRING','DICTIONARY', 'DICTARRAY', 'DICTDICT']:
            self.read_return_type = r_type
        else:
            print("ERROR: return type not supported")

    def read(self, f_path=None):
        rp = self.__check__(f_path)
        if rp == None:
            print("ERROR: no path provided")
            return
        
        with open(rp, 'r') as csvfile:
            csvreader=csv.reader(csvfile)
            if self.read_return_type == 'DICTARRAY':
                return list(csv.DictReader(csvfile))
            elif self.read_return_type == 'DICTDICT':
                dict_headers=next(csvreader)
                dataset_dict={}
                for row in csvreader:
                    dataset_dict[row[0]]={dict_headers[i]:row[i] for i in range(1, len(dict_headers))}
                return dataset_dict
            return list(csv.reader(csvfile))
    
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