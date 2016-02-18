from __future__ import division
from Patient import Patient
from decimal import *
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

# helper methods used by model to filter patients inside model
# these are generator methods; they create generator objects that contain 
# a patient in each node and are easily translated into lists which are a bit
# more maleable in python.
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
    # The following wall of code uses the above helper methods to generate lists of the various types; females, males, with virus, without virus
    # etc.
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
    positive_blood_no_virus = list(filter_blood_negative(data, "+"))
    positive_blood_no_virus_count = len(positive_blood_no_virus)
    negative_blood_with_virus = list(filter_blood_positives(data, "-"))
    negative_blood_with_virus_count = len(negative_blood_with_virus)
    negative_blood_no_virus = list(filter_blood_negative(data, "-"))
    negative_blood_no_virus_count = len(negative_blood_no_virus)
    heavy_weight_with_virus = list(filter_weight_heavy_positives(data))
    heavy_weight_with_virus_count = len(heavy_weight_with_virus)
    heavy_weight_no_virus = list(filter_weight_heavy_negatives(data))
    heavy_weight_with_no_count = len(heavy_weight_no_virus)
    light_weight_with_virus = list(filter_weight_light_positives(data))
    light_weight_with_virus_count = len(light_weight_with_virus) 
    light_weight_no_virus = list(filter_weight_light_negatives(data))
    light_weight_with_no_count = len(light_weight_no_virus)


    # calculating likelihoods using Decimal division
    prior_not_virus = (Decimal(no_virus_count) / Decimal(patient_count))
    prior_virus = (Decimal(with_virus_count) / Decimal(patient_count))
    liklihood_gender_female_positive = (Decimal(female_positive_count) / Decimal(with_virus_count))
    liklihood_gender_female_negative = (Decimal(female_negative_count) / Decimal(no_virus_count))
    liklihood_gender_male_positive = 1 - liklihood_gender_female_positive
    liklihood_gender_male_negatives = 1 - liklihood_gender_female_negative
    liklihood_blood_positive_with_virus = (Decimal(positive_blood_with_virus_count) / Decimal(with_virus_count))
    liklihood_negative_blood_with_virus = (Decimal(negative_blood_with_virus_count) / Decimal(with_virus_count))
    liklihood_positive_blood_no_virus = (Decimal(positive_blood_no_virus_count) / Decimal(no_virus_count))
    liklihood_negative_blood_no_virus = (Decimal(negative_blood_no_virus_count / Decimal(no_virus_count)))
    liklihood_for_weights_heavy_with_virus = (Decimal(heavy_weight_with_virus_count) / Decimal(with_virus_count))
    liklihood_for_weights_heavy_no_virus = (Decimal(heavy_weight_with_no_count) / Decimal(no_virus_count))
    liklihood_for_weights_light_with_virus = (Decimal(light_weight_with_virus_count) / Decimal(with_virus_count))
    liklihood_for_weights_light_no_virus = (Decimal(light_weight_with_no_count) / Decimal(no_virus_count))

    print("prior for not virus: " + str(prior_not_virus))
    print("prior for with virus: " + str(prior_virus))
    print("likelihood for female given virus: " + str(liklihood_gender_female_positive))
    print("likelihood for female given not virus: " + str(liklihood_gender_female_negative))
    print("likelikhood for male given virus: " + str(liklihood_gender_male_positive))
    print("likelikhood for male given not virus: " + str(liklihood_gender_male_negatives))
    print("likelihood for blood positive given virus: " + str(liklihood_blood_positive_with_virus))
    print("likelikhood for blood negative given virus: " + str(liklihood_negative_blood_with_virus))
    print("likelikhood for blood positive given not virus: " + str(liklihood_positive_blood_no_virus))
    print("likelikhood for blood negative given not virus: " + str(liklihood_negative_blood_no_virus))
    print("likelihood for weight > 170 given virus: " + str(liklihood_for_weights_heavy_with_virus))
    print("likelihood for weight > 170 given not virus: " + str(liklihood_for_weights_heavy_no_virus))
    print("likelihood for weight <= 170 given virus: " + str(liklihood_for_weights_light_with_virus))
    print("likelihood for weight <= 170 given not virus: " + str(liklihood_for_weights_light_no_virus))

    # prediction stuff
    NN = NY = YN = YY = 0 

    line = 1
    test = []
    test = build_array("proj1test.txt")
    test_with_virus_list = list(filter_virus(test, "Y"))
    test_with_virus_count = len(test_with_virus_list)
    test_no_virus_list = list(filter_virus(test, "N"))
    test_no_virus_count = len(test_no_virus_list)

    print(str(len(test)) + "size of test data")
    for n in test:
        no_virus = test_no_virus_count
        yes_virus = test_with_virus_count
        if (n.gender == "male"):
            no_virus *= liklihood_gender_male_negatives
            yes_virus *= liklihood_gender_male_positive
        else:
            no_virus *= liklihood_gender_female_negative
            yes_virus *= liklihood_gender_female_positive
        if (n.blood.endswith("+")):
            no_virus *= liklihood_positive_blood_no_virus
            yes_virus *= liklihood_blood_positive_with_virus
        else:
            no_virus *= liklihood_negative_blood_no_virus
            yes_virus *= liklihood_negative_blood_with_virus
        if (n.weight > 170):
            no_virus *= liklihood_for_weights_heavy_no_virus
            yes_virus *= liklihood_for_weights_heavy_with_virus
        else:
            no_virus *= liklihood_for_weights_light_no_virus
            yes_virus *= liklihood_for_weights_light_with_virus
        if (yes_virus >= no_virus):
            prediction = True
        else:
            prediction = False
        if (n.virus == "Y"):
            if (prediction):
                YY += 1
            else:
                YN += 1
        else:
            if (prediction):
                NY += 1
            else:
                NN += 1
        actual = str(n.virus)
        predicted = "Y" if prediction else "N"
        print(str(line) + " " + actual + " " + predicted)

    print("\nConfusion matrix\n")
    print("        Predicted Class\n")
    print("Actual    "+str(YY)+"        "+str(NY)+"\nClass       "+ str(YN) + "      " +str(NN))


model()

