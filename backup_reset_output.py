import os, shutil

#todo: add auto monthly backup and reset for file
 

def reset_outfile():
	headers = 'date, startloc, endloc, startodo, endodo, tripmiles\n'
	# erase all data from outfile and initialize headers
	with open('output.txt', 'w') as file:
		file.write(headers)
	
	with open('output.txt', 'r') as file:
		if file.readline() == headers:
			print('Resetting output.txt... Done.')
		else:
			print('There was an error overwriting output.txt')
			
#todo: add date recognition for new month feature
def backup_outfile(file):
	backup_dir = os.path.basename('backups')
	number = 1
	while True:
		filename = os.path.basename(file) + '_' + str(number) + '.txt'
		
		
		if not os.path.exists(backup_dir + '/' + filename):
			shutil.copy2('output.txt', backup_dir + '/' + filename)
			print(f'Backup of output.txt successful as backups/{filename}.')
			break
		number = number + 1
		

backup_outfile('output')			
reset_outfile()
