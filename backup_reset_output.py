#mileage backup_reset_output.py

import os, shutil
import config


#todo: add auto monthly backup and reset for file
 

def reset_outfile(file):
	headers = 'date, startloc, endloc, startodo, endodo, tripmiles\n'
	# erase all data from outfile and initialize headers
	with open(file, 'w') as f:
		f.write(headers)
	
	with open(file, 'r') as f:
		if f.readline() == headers:
			print(f'Resetting {file}... Done.')
		else:
			print(f'There was an error overwriting {file}')
			
#todo: add date recognition for new month feature
def backup_outfile(file):
	backup_dir = os.path.basename('backups')
	number = 1
	while True:
		filename = os.path.basename(config.output_file) + '_' + str(number) + '.txt'
		
		
		if not os.path.exists(backup_dir + '/' + filename):
			shutil.copy2(file, backup_dir + '/' + filename)
			print(f'Backup of {file} successful as backups/{filename}.')
			break
		number = number + 1
		

backup_outfile(config.output_file)			
reset_outfile(config.output_file)
