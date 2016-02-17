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
        if el.gender == value:
            yield el

# method to filter patients by virus
def filter_virus(patients, value):
    for el in patients:
        if el.virus == value:
            yield el

# method to filter patients by sex for positive
def filter_gender_positives(patients, value):
    for el in patients:
        if (el.gender == value and el.virus == "Y"):
            yield el


def filter_blood_positives(patients, value):
    for el in patients:
        if (el.blood.endswith(value) and el.virus == "Y"):
            yield el


def filter_blood_negative(patients, value):
    for el in patients:
        if (el.blood.endswith(value) and el.virus == "N"):
            yield el


# these are broken
def filer_weight_heavy_positives(patients):
    for el in patients:
        if (el.weight > 170 and el.virus == "Y"):
            yield el


def filer_weight_heavy_negatives(patients):
    for el in patients:
        if (el.weight > 170 and el.virus == "N"):
            yield el


def filter_weight_light_positives(patients):  # add virus stuff
    for el in patients:
        if (el.weight <= 170 and el.virus == "Y"):
            yield el


def filter_weight_light_negatives(patients):  # add virus stuff
    for el in patients:
        if (el.weight <= 170 and el.virus == "N"):
            yield el


def main():
    data = []
    data = build_array()
    print(str(len(data)) + " Patients total")
    
    patient_count = len(data)

    # the next few lines build a list of Male, Females, Patients with virus, Patients witout virus, Male Positives, Female positives, etc.
    # then prints out the size of these lists.  This is not idiomatic python, object orientation came later on and feels kinda clunky but works.
    males = list(filter_gender(data, "male"))
    females = list(filter_gender(data, "female"))
    print(str(len(females)) + " Females")
    female_count = len(females)
    print(str(len(males)) + " Males")
    males_count = len(males)

    with_virus_list = list(filter_virus(data, "Y"))
    with_virus_count = len(with_virus_list)
    no_virus_list = list(filter_virus(data, "N"))
    no_virus_count = len(no_virus_list)

    print(str(len(with_virus_list)) + " Patients with virus")
    print(str(len(no_virus_list)) + " Patients without virus")

    male_virus_list = list(filter_gender_positives(data, "male"))
    female_virus_list = list(filter_gender_positives(data, "female"))
    print(str(len(male_virus_list)) + " Males with virus")
    print(str(len(female_virus_list)) + " Female with virus")
    female_positive_count = len(female_virus_list)
    female_negative_count = female_count - female_positive_count

    positive_blood_with_virus = list(filter_blood_positives(data, "+"))
    positive_blood_with_virus_count = len(positive_blood_with_virus)
    print(str(positive_blood_with_virus_count) + " Positive blood type who have virus")
    
    negative_blood_with_virus = list(filter_blood_positives(data, "-"))
    negative_blood_with_virus_count = len(negative_blood_with_virus)
    print(str(negative_blood_with_virus_count) + " Negative blood type who have virus")

    # likelihood for weight: p(weight >= 170 | virus=y), p(weight>170 | virus=n)
    heavy_weight_with_virus = list(filer_weight_heavy_positives(data))
    heavy_weight_with_virus_count = len(heavy_weight_with_virus)
    print(str(heavy_weight_with_virus_count) + " Above 170LBS with virus")

    # liklihood for weight: p(weight < 170 | virus = y)
    light_weight_with_virus = list(filter_weight_light_positives(data))
    light_weight_with_virus_count = len(light_weight_with_virus)
    print(str(light_weight_with_virus_count) + " Equal or Below 170lbs with virus (fix me plz)")


    print("\n\nStart of Model Calculations\n")

    # priors for the probability of both patients who have the virus and those that do not: p(virus=y), p(virus=n).
    prior_not_virus = (float(no_virus_count) / float(patient_count))
    print(str(prior_not_virus) + " p(patient | virus = n)")
    prior_virus = (float(with_virus_count) / float(patient_count))
    print(str(prior_virus) + " p(patient | virus = y)\n\n")
    
    # p(gender = f | virus = y)
    liklihood_gender_female_positive = (float(female_positive_count) / float(with_virus_count))
    print(str(liklihood_gender_female_positive) + " p(gender =f | virus = y)")
    
    liklihood_gender_female_negative = (float(female_negative_count) / float(no_virus_count))
    print(str(liklihood_gender_female_negative) + " p(gender =f | virus = n)")
    
    liklihood_gender_male_positive = 1 - liklihood_gender_female_positive
    print(str(liklihood_gender_male_positive) + " p(gender =m | virus =y)")
    
    liklihood_gender_male_negatives = 1 - liklihood_gender_female_negative
    print(str(liklihood_gender_male_negatives) + " p(gender =m | virus =n)\n")

    # liklihood_blood_types 
    # p(type = + | virus = y)
    # p(type = - | virus = n) 
    liklihood_blood_positive_with_virus = (float(positive_blood_with_virus_count) / float(with_virus_count))
    print(str(liklihood_blood_positive_with_virus) + " p(type = + | virus = y)")
    liklihood_positive_blood_no_virus = 1 - liklihood_blood_positive_with_virus
    print(str(liklihood_positive_blood_no_virus) + " p(type = + | virus = n)")

    liklihood_negative_blood_with_virus = (float(negative_blood_with_virus_count) / float(with_virus_count))
    print(str(liklihood_negative_blood_with_virus) + " p(type = - | virus = y)")
    liklihood_negative_blood_no_virus = 1 - liklihood_negative_blood_with_virus
    print(str(liklihood_negative_blood_no_virus) + " p(type = - | virus = n)")

    # liklihood_for_weights
    # p(weight > 170 | virus = y) 
    liklihood_for_weights_heavy_with_virus = (float(heavy_weight_with_virus_count) / float(with_virus_count))
    print(str(liklihood_for_weights_heavy_with_virus) + " p(weight > 170 | virus = Y) (fix me plz)")

    liklihood_for_weights_light_with_virus = (float(light_weight_with_virus_count) / float(with_virus_count))
    print(str(liklihood_for_weights_light_with_virus) + " p(weight < 170 | virus = Y) (fix me plz)")



    # todo finish weights part, stuff all that shit into a model object of variables. start on predictions method

main()