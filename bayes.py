from Patient import Patient
import csv


def build_array(file_to_open):
    patient_array = []

    try:
        training_reader = csv.reader(open(file_to_open))
        for row in training_reader:
            training = Patient((int(row[0])), row[1], row[2], row[3], row[4])
            patient_array.append(training)
    except Exception as e:
        print(e)
    return patient_array

# helper methods used by model to filter patient
def filter_gender(patients, value):
    for el in patients:
        if el.gender == value:
            yield el


def filter_virus(patients, value):
    for el in patients:
        if el.virus == value:
            yield el


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


def filter_weight_heavy_positives(patients):
    for el in patients:
        if (int(el.weight) > 170 and el.virus == "Y"):
            yield el


def filter_weight_heavy_negatives(patients):
    for el in patients:
        if (int(el.weight) > 170 and el.virus == "N"):
            yield el


def filter_weight_light_positives(patients):  # add virus stuff
    for el in patients:
        if (int(el.weight) <= 170 and el.virus == "Y"):
            yield el


def filter_weight_light_negatives(patients):  # add virus stuff
    for el in patients:
        if (int(el.weight) <= 170 and el.virus == "N"):
            yield el


def model():
    data = []
    data = build_array("proj1train.txt")
    
    patient_count = len(data)
    males = list(filter_gender(data, "male"))
    females = list(filter_gender(data, "female"))
    female_count = len(females)
    males_count = len(males)
    with_virus_list = list(filter_virus(data, "Y"))
    with_virus_count = len(with_virus_list)
    no_virus_list = list(filter_virus(data, "N"))
    no_virus_count = len(no_virus_list)
    male_virus_list = list(filter_gender_positives(data, "male"))
    female_virus_list = list(filter_gender_positives(data, "female"))
    female_positive_count = len(female_virus_list)
    female_negative_count = female_count - female_positive_count
    positive_blood_with_virus = list(filter_blood_positives(data, "+"))
    positive_blood_with_virus_count = len(positive_blood_with_virus)
    negative_blood_with_virus = list(filter_blood_positives(data, "-"))
    negative_blood_with_virus_count = len(negative_blood_with_virus)
    heavy_weight_with_virus = list(filter_weight_heavy_positives(data))
    heavy_weight_with_virus_count = len(heavy_weight_with_virus)
    light_weight_with_virus = list(filter_weight_light_positives(data))
    light_weight_with_virus_count = len(light_weight_with_virus) 
    
    #helper print statements 
    
    print(str(len(males)) + " Males")
    print(str(len(females)) + " Females")
    print(str(len(with_virus_list)) + " Patients with virus")
    print(str(len(no_virus_list)) + " Patients without virus")
    print(str(len(male_virus_list)) + " Males with virus")
    print(str(len(female_virus_list)) + " Female with virus")
    print(str(positive_blood_with_virus_count) + " Positive blood type who have virus")
    print(str(negative_blood_with_virus_count) + " Negative blood type who have virus")
    print(str(heavy_weight_with_virus_count) + " Above 170LBS with virus")
    print(str(light_weight_with_virus_count) + " Equal or Below 170lbs with virus")
    print("\n\nStart of Model Calculations\n")

    prior_not_virus = (float(no_virus_count) / float(patient_count))
    print("prior for not virus: " + str(prior_not_virus))
    
    prior_virus = (float(with_virus_count) / float(patient_count))
    print("prior for with virus: " + str(prior_virus))
    
    liklihood_gender_female_positive = (float(female_positive_count) / float(with_virus_count))
    print("likelihood for female given virus: " + str(liklihood_gender_female_positive))
    
    liklihood_gender_female_negative = (float(female_negative_count) / float(no_virus_count))
    print("likelihood for female given not virus: " + str(liklihood_gender_female_negative))
    
    liklihood_gender_male_positive = 1 - liklihood_gender_female_positive
    print("likelikhood for male given virus: " + str(liklihood_gender_male_positive))
    
    liklihood_gender_male_negatives = 1 - liklihood_gender_female_negative
    print("likelikhood for male given not virus: " + str(liklihood_gender_male_negatives))



    liklihood_blood_positive_with_virus = (float(positive_blood_with_virus_count) / float(with_virus_count))
    print("likelihood for blood positive given virus: " + str(liklihood_blood_positive_with_virus))
    
    liklihood_positive_blood_no_virus =  1 - liklihood_negative_blood_no_virus
    print("likelikhood for blood positive given not virus: " + str(liklihood_positive_blood_no_virus))

    liklihood_negative_blood_with_virus = (float(negative_blood_with_virus_count) / float(with_virus_count))
    print("likelikhood for blood negative given virus: " + str(liklihood_negative_blood_with_virus))

    liklihood_negative_blood_no_virus = 1 - liklihood_positive_blood_no_virus
    print("likelikhood for blood negative given not virus: " + str(liklihood_negative_blood_no_virus))




    liklihood_for_weights_heavy_with_virus = (float(heavy_weight_with_virus_count) / float(with_virus_count))
    print("likelihood for weight > 170 given virus: " + str(liklihood_for_weights_heavy_with_virus))
    
    liklihood_for_weights_heavy_no_virus = 1 - liklihood_for_weights_heavy_with_virus
    print("likelihood for weight > 170 given not virus: " + str(liklihood_for_weights_heavy_no_virus))
    
    liklihood_for_weights_light_with_virus = (float(light_weight_with_virus_count) / float(with_virus_count))
    print("likelihood for weight <= 170 given virus: " + str(liklihood_for_weights_light_with_virus))

    liklihood_for_weights_light_no_virus = 1 - liklihood_for_weights_light_with_virus
    print("likelihood for weight <= 170 given not virus: " + str(liklihood_for_weights_light_no_virus))




model()

