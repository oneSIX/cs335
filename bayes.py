from Patient import Patient
import csv
# 

def build_array():
	patient_array = []

	try:
		training_reader = csv.reader(open("proj1train.txt"))
		for row in training_reader:
			training = Patient((int(row[0])), row[1], row[2], row[3], row[4])
			patient_array.append(training)
	except Exception as e:
		print(e)
	# for row in test_reader:
	# 	key = row[0]
	# 	test[key] = row[1:]

	# for row in playdata:
	# 	key = row[0]
	# 	play[key] = row[1:]
	# print(len(patient_array))
	return patient_array

# patients = build_array()

# method to filter patients by gender
def filter_gender(patients, value):
	for el in patients:
		if el.gender==value: yield el

# method to filter patients by virus
def filter_virus(patients, value):
	for el in patients:
		if el.virus==value: yield el

# method to filter patients by sex
def filter_gender_positives(patients, value):
	for el in patients:
		if (el.gender==value and el.virus=="Y"): yield el

def filter_blood_positive(patients):
	for el in patients:
		if (el.blood == "A+" or el.blood == "B+" or el.blood == "O+"): yield el

def filter_blood_negative(patients):
	for el in patients:
		if (el.blood == "A-" or el.blood == "B-" or el.blood == "O-"): yield el


def main():
	data = []
	data = build_array()
	print(str(len(data)) + " Patients total")
	
	# the next few lines build a list of Male, Females, Patients with virus, Patients witout virus, Male Positives, Female positives, etc.
	# then prints out the size of these lists.  This is not idiomatic python, object orientation came later on and feels kinda clunky but works.
	males = list(filter_gender(data, "male"))
	females = list(filter_gender(data, "female"))
	print(str(len(females)) + " Females")
	print(str(len(males)) + " Males")

	virus_positives = list(filter_virus(data, "Y"))
	virus_negatives = list(filter_virus(data, "N"))
	print(str(len(virus_positives)) + " Patients positive for virus")
	print(str(len(virus_negatives)) + " Patients negative for virus")

	male_positives = list(filter_gender_positives(data, "male"))
	female_positives = list(filter_gender_positives(data, "female"))
	print(str(len(male_positives)) + " Male positives")
	print(str(len(female_positives)) + " Female positives")


main()