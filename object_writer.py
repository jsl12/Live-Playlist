import pickle


class ObjectWriter():
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass
    
    def write(self, new_data):
        self.data = new_data
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)
            
            
if __name__ == '__main__':
    sw = ObjectWriter('object_writer.test')
    if sw.data:
        print(sw.data)
    print("Writing to file")
    sw.write(set([1,2,3,4,5,1,2]))