##########  configuration ########################
log_file = r'log_file.txt'
data_file = r'data.txt'
cred_file = r'cred.txt'
school_name = "Sainik Public School"
##################################################
width = 60
phash = '-'*width
debug =False
all_percentage = []
##################################################


def _log(level,mesg):
	mesg = f'[ {level} ] : {mesg} \n'
	if debug:
		print(mesg)
	else:
		fh = open(log_file, 'a')
		fh.write(mesg)
		fh.close()


def log_error(mesg):
	_log('ERROR', mesg)


def log_info(mesg):
	_log('INFO', mesg)


def pheader():
	print(f"{phash}\n{school_name.center(width)}\n{phash}\n")


def fist_screen():
	pheader()
	print("Enter your choice from below menu :")
	print("1 : Teachers Login")
	print("2 : Students Login\n")
	choice = input("Enter your choice : ")
	log_info(f'Login type selected - {choice}')
	return choice


def login_screen(type):
	mesg = f"{type} Login Console"
	print(f'\n{phash}\n{mesg.center(width)}\n{phash}')
	uname = input(f"Enter {type} user name : ")
	paswd = input("Enter password : ")
	log_info(f"{type} uname : {uname}")
	return uname,paswd


def verify_cred_data(uname,paswd):
	log_info(f'Verify user {uname}')
	fh = open(cred_file)
	for line in fh:
		u,p = line.split(',')
		p = p.strip()
		if u == uname and p == paswd:
			log_info(f"{uname} : password matched")
			fh.close()
			return True
		elif u == uname and p != paswd:
			log_info(f"{uname} : password NOT matched")
			fh.close()
			return False
	log_info(f"{uname} : User Not Found")
	fh.close()
	return False


def pcommon_choice_menu():
	print('1 : Get Result')
	print('2 : Search Roll No')


def teacher_choice_menu():
	pheader()
	pcommon_choice_menu()
	print('3 : Enter student info')
	choice = input("Enter your choice : ")
	log_info(f'Choice type selected - {choice}')
	return choice


def student_choice_menu():
	pheader()
	pcommon_choice_menu()
	choice = input("Enter your choice : ")
	log_info(f'Choice type selected - {choice}')
	return choice

def ask_stud_info():
	pheader()
	print(' \n Enter Students information \n ')
	name = input("Enter student name : ")
	m_eng = input("Enter students English marks :")
	m_sci = input("Enter students Science marks :")
	m_maths = input("Enter students Maths marks :")
	return {'name': name, 'm_eng': m_eng, 'm_sci': m_sci, 'm_maths': m_maths}


def get_total_students():
	fh = open(data_file)
	total = len(fh.readlines())
	fh.close()
	return total


def store_student_info():
	info = list(ask_stud_info().values())
	percentage = (int(info[1]) + int(info[2]) + int(info[3])) * .3
	percentage = format(percentage, '.2f')
	r_no = get_total_students() + 1
	fh = open(data_file,'a')
	data = ','.join(info)
	fh.write(f'{r_no},{data},{percentage}\n')
	fh.close()
	refresh_global_percentage_data()


def student_flow():
	while True:
		ch = student_choice_menu()
		log_info('Student choice is {ch}')
		if ch == '2':
			search_student_roll()
		elif ch == '1':
			print_result()
		else:
			break


def teacher_flow():
	u, p = login_screen('Teachers')
	if not verify_cred_data(u, p):
		print(' \n Invalid Login \n ')
		return
	while True:
		ch = teacher_choice_menu()
		if ch == '3':
			store_student_info()
		elif ch == '2':
			search_student_roll()
		elif ch == '1':
			print_result()
		else:
			break


def print_result():
	pheader()
	r_no = input('Enter Students Roll no : ')
	data = get_student_data(r_no)
	if data:
		data = data.split(',')
		log_info(data)
		log_info(f"Get Rank for percentage : {data[-1].strip()}")
		log_info(all_percentage)
		rank = all_percentage.index(data[-1].strip()) + 1
		p_result_format(data,rank)
	else:
		print('\n Invalid Roll Number \n')


def p_result_format(data,rank):
	pheader()
	print(f'Name        : {data[1]}')
	print(f'Roll Number : {data[0]}')
	print(phash)
	print(f'English     : {data[2]}')
	print(f'Science     : {data[3]}')
	print(f'Maths       : {data[4]}')
	print(phash)
	print(f'Percentage  :  {data[5].strip()}')
	print(f'Rank       :  {rank}')
	print(phash)


def get_student_data(r_no):
	fh = open(data_file)
	for line in fh:
		if r_no == line.split(',')[0]:
			log_info(f"student data : {line}")
			fh.close()
			return line


def search_student_roll():
	pheader()
	name = input("Enter the name to search : ")
	data = get_stud_roll_no(name)
	if data:
		lwidth = width//2
		print(f"{'Name'.ljust(lwidth)} {'Roll Number'.rjust(lwidth)}")
		for d in data:
			print(f'{d[1].ljust(lwidth)} {d[0].rjust(lwidth)}')
	else:
		print(f"{name} NOT Found !! ")


def refresh_global_percentage_data():
	global all_percentage
	all_percentage = []
	fh = open(data_file)
	for line in fh:
		all_percentage.append(line.split(',')[-1].strip())
	all_percentage = list(set(all_percentage))
	all_percentage.sort()
	all_percentage.reverse()
	fh.close()


def get_stud_roll_no(name):
	fh = open(data_file)
	r_nos = []
	for line in fh:
		if name in line:
			data = line.split(',')[:2]
			r_nos.append(data)
	fh.close()
	return r_nos


def main():
	refresh_global_percentage_data()
	ch = fist_screen()
	if ch == '1':
		teacher_flow()
	elif ch == '2':
		student_flow()


main()