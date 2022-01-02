def dict_data_cleaner(dict_data, item=''):
    return_data={}
    for d in dict_data:
        if dict_data[d]!=item:
            return_data[d]=dict_data[d]
    return return_data

def list_dict_cleaner(list_dict_data):
    for i in range(len(list_dict_data)):
        list_dict_data[i] = dict_data_cleaner(list_dict_data[i])
    return list_dict_data