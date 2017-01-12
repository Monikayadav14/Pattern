import csv
import re
import xlsxwriter
from operator import itemgetter


file_name = "all_delivered.csv"


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


def get_pattern(file_data, column_name):
	format_freq_dist = {}

	for x in file_data:

		new_id = re.sub(r'[a-zA-Z]', "A", x[column_name])
		new_id1 = re.sub(r'[0-9]', "9", new_id)
		if [' '] == list(set(list(new_id1))):
			new_id1 = 'space'
		format_freq_dist.setdefault(new_id1, 0)
		format_freq_dist[new_id1] += 1

	return format_freq_dist


def get_value(file_data, column_name):
	value_freq_dist = {}

	for row in file_data:
		# for j in row:
		value_freq_dist.setdefault(row[column_name], 0)
		value_freq_dist[row[column_name]] += 1
	return value_freq_dist


# def writeToCSV(filename, contents_to_write, keys):
# 	# PURPOSE:
# 	#       This function reads the contents of a List of Dictionaries,
# 	#       and stores them in a csv file.
# 	with open(filename, 'wb') as f:
# 		w = csv.DictWriter(f, keys)
# 		w.writeheader()
# 		for row in contents_to_write:
# 			w.writerow(row)
# 	return True


def Write_To_Excel(final_list, final_list1):
	wb = xlsxwriter.Workbook('Result.xlsx')
	ws_format = wb.add_worksheet("ws_format")
	ws_value = wb.add_worksheet('ws_value')
	ws_summary  = wb.add_worksheet('Summary')
	ws_format.write(0, 0, 'Format')
	ws_format.write(0, 1, 'Occurances')
	ws_format.write(0, 2, 'Length')
	ws_value.write(0, 0, 'Value')
	ws_value.write(0,1,'Ocuurances')
	ws_value.write(0, 2, 'Length')
	Total_rows = len(final_list)
	for row in range(0,Total_rows):
		column = 0
		for keys in ['Format', 'Occurances','Length']:
			ws_format.write(row+1, column, final_list[row][keys])
			column = column + 1
	Total_rows1 = len(final_list1)
	for row in range(0, Total_rows1):
		column = 0
		for keys in ['Value', 'Occurances','Length']:
			ws_value.write(row + 1, column, final_list1[row][keys])
			column = column + 1

	ws_summary.write(0, 0, s1)
	ws_summary.write(1, 0, s2)
	ws_summary.write(2, 0, mx)
	ws_summary.write(3, 0, mn)
	ws_summary.write(4, 0, format_max)
	ws_summary.write(5, 0, value_max)
	wb.close()
	return wb

if __name__ == '__main__':
	final_list =[]
	final_list1 = []
	column_list = ['address']
	for column in column_list:
		file_data = get_csv_records(file_name)
		myresults = get_pattern(file_data, column)
		finalresult = get_value(file_data, column)

		for item in myresults:
			d1={
				'Format':item,
				'Occurances':myresults[item],
			}
			if item == 'space':
				d1['Length'] = 0

			else:
				d1['Length'] = len(item)

			final_list.append(d1)
		final_list_sort = sorted(final_list,key=itemgetter('Length'),reverse=True)
		mx = "Maximum Length is %s" %final_list_sort[0]['Length']
		mn = "Minimum Length is %s" %final_list_sort[-1]['Length']
		final_list_Occ_sort = sorted(final_list, key=itemgetter('Occurances'), reverse=True)
		format_max = "Most common format is %s" %final_list_Occ_sort[0]['Format']

		for item in finalresult:
			d2 = {
				'Value':item,
				'Occurances':finalresult[item]
			}
			if item == 'space':
				d2['Lenght'] = 0
			else:
				d2['Length'] =len(item)
			final_list1.append(d2)
		final_list1_Occ_sort = sorted(final_list1, key=itemgetter('Occurances'), reverse =True)
		value_max = "Most common value is (%s)" % final_list1_Occ_sort[0]['Value']

		cardinality = ((len(final_list)*100)/float(len(file_data)))
		cardinality1 = ((len(final_list1)*100)/float(len(file_data)))

		s1 = "cardinality of pattern is " + str(cardinality)
		s2 = "cardinality of value is " + str(cardinality1)
		# writeToCSV("all_format_add.csv",final_list, ['Format', 'Occurances'])
		# writeToCSV("all_value_add.csv",final_list1, ['Value', 'Occurances'])
	Write_To_Excel(final_list, final_list1)