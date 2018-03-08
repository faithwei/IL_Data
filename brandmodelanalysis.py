dashboard_list = []

def read_file_by_iteration(file_name):
	
	with open(file_name) as my_file:
		for line in my_file:
			dashboard.append(line)
		return dashboard_list

print read_file_by_iteration(dashboard.txt)