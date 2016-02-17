

class Patient(object):
	# id = 0
	# gender = ""
	# virus = None
	# blood = ""
	# weight = 0

	def __init__(self, id, gender, blood, weight, virus):
		super(Patient, self).__init__()
		self.id = id
		self.gender = gender
		self.blood = blood
		self.weight = weight
		self.virus = virus