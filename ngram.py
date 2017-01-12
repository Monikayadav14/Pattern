import csv

file_name = "Kaithal_add.csv"

def get_csv_records(file_name):
	data = open(file_name)
	reader = csv.reader(data)
	records_list = []
	keys = reader.next()

	for row in reader:
		record_dict = dict(zip(keys, row))
		records_list.append(record_dict)
	data.close()
	return records_list


def make():
	master_dict = {}
	for adr in file_data:
		for word in adr:
			split_words = word.split(" ")
			for x in adr:
				master_dict.setdefault(x,0)
				master_dict[x] += 1
	return master_dict


def writeToCSV(filename, contents_to_write, keys):
	# PURPOSE:
	#       This function reads the contents of a List of Dictionaries,
	#       and stores them in a csv file.
	with open(filename, 'wb') as f:
		w = csv.DictWriter(f, keys)
		w.writeheader()
		for row in contents_to_write:
			w.writerow(row)
	return True

if __name__ == '__main__':
	file_data = get_csv_records(file_name)
	myresult = make()
	#writeToCSV("unigram",myresult,["rec","count"])
	print myresult
	print file_data

# Tasks'links': "maps.google.com/?q="+item+"tushar"
#       1. Write a function to read addresses from a csv
#       2. Function to write a csv
#       3. Create strings which will act as links to google maps