#! python3
# randomChoreAssign.py - Randomly assigns list of chores to list of people,
# and emails each their assigned chore.

import ast, os, random, re, smtplib

family_path = os.path.join(os.getcwd() + '\\family.txt')
log_path = os.path.join(os.getcwd() + '\\log.txt')

family = {}

# For recurring runs.
if os.path.exists(family_path):

	# Read and save the dict of family members.
	family_file = open(family_path, 'r')
	family = ast.literal_eval(family_file.read())
	family_file.close()

	pass

# For first-time runs.
else:

	# If log_file doesn't exist, write family members.
	while True:
	
		new_family = input('Please input a family member\'s name: ')
		new_email = input('Please input a family member\'s email: ')

		family[new_family] = new_email
		
		prompt = input('Are there any additional family members? ')
		
		if re.search(r'^y', prompt, flags=re.IGNORECASE):
			pass
			
		else:

			# Write family to txt file for later reference.
			family_file = open(family_path, 'w')
			family_file.write(str(family))
			family_file.close()

			break

chores_master = ['bathroom', 'dishes', 'floor', 'kitchen', 'laundry']

# Log into email server.
my_email = input('Please enter your email address: ')
my_password = input('Please enter your password: ')

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(my_email, my_password)

# Stored separately as list will be popped off.
chores = chores_master.copy()

assignments = {}
prev_assignments = {}

# Populate previous assignments.
if os.path.exists(log_path):
	prev_assign_file = open(log_path, 'r')
	prev_assignments = ast.literal_eval(prev_assign_file.read())
	prev_assign_file.close()

# Family member, family member's email address.
for k, v in family.items():

	# If log is already populated, pick a chore at random then check for previous assignments.
	if len(prev_assignments) > 0:
		while True:
			random_chore = random.choice(chores)

			# If the choice is different that than the previous, proceed.
			if random_chore != prev_assignments[k]:
				break

	# Else fetch a chore at random.
	else:
		random_chore = random.choice(chores)
	
	# Pop the core from the list.
	chores.remove(random_chore)

	# Send as email.
	email_message = 'Subject: This Week\'s Chore Assignment.\n' +\
		'Dear %s,\n\nYour assignment this week is to clean the %s.\n\nMuch appreciated!' %\
		(k, random_chore)
	
	print('Sending message to %s...' % v)
	
	send_status = smtpObj.sendmail(my_email, v, email_message)
	
	# Check for any errors.
	if send_status != {}:
		print('There was a problem sending to %s: %s.' % (v, send_status))
	
	# Write the chore to assignments to be logged.
	assignments[k] = random_chore

# Close the email object.
smtpObj.quit()

# Save assignments to the log for future reference.
# Opening in write mode rewrites all content to null.
log_file = open(log_path, 'w')
log_file.write(str(assignments))
log_file.close()

print('All assignments have been sent out. Great job, everybody!')
