import object_writer
import saving_artistplaylist

def main():
    writer = object_writer.ObjectWriter(saving_artistplaylist.SAVE_FILE)
    data = writer.data
    for d in data:
        print(d)

if __name__ == '__main__':
    main()
