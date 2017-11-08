class Mur(object):
	@staticmethod
	def execute():
		setDebugString("Je suis Mur")

		percepts = getPercepts()

		actionWarEngineer.nextState = Mur

		if isBlocked():
			RandomHeading()
			return move()

		#tant que je ne suis pas arriver a la base
		if (not actionWarEngineer.arriver):
			#si je me dirige vers une base
			if (actionWarEngineer.base):
				setDebugString("je suis dedant")
				#pour tous se que je voit
				for percept in getPerceptsAllies():
					#si c'est une base allies
					if (percept.getType().equals(WarAgentType.WarBase)):
						#si je suis arriver a la base
						if (percept.getDistance() <= 5):
							actionWarEngineer.arriver = True
							RandomHeading()
							setHeading(getHeading() + 180)
							return idle()
							
				for msg in getMessages():
					#si la base fais coucou
					if msg.getMessage() == "Je suis la base":
						#je fonce vers la base
						setHeading(msg.getAngle())
				return move()
			#si je me dirige pas vers une base
			else:
				#pour tous les messages
				for msg in getMessages():
					#si la base fais coucou
					if msg.getMessage() == "Je suis la base":
						#je fonce vers la base
						setHeading(msg.getAngle())
						actionWarEngineer.base = True
						return move()
		#quand je suis a la base si le premier mur n'est pas creer
		elif (not actionWarEngineer.premiermur):
			#si je ne suis pas a 60 de distance de la base
			if (actionWarEngineer.distancebase < 60):
				actionWarEngineer.distancebase = actionWarEngineer.distancebase + 1
				return move()
			#si je suis a 60 de la base
			elif (actionWarEngineer.distancebase == 60):
				actionWarEngineer.distancebase = actionWarEngineer.distancebase + 1
				setNextBuildingToBuild(WarAgentType.Wall)
				return build()
			#je me tourne pour aller construire le deuxieme mur
			else:
				setHeading(getHeading()+ 85)
				actionWarEngineer.premiermur = True
				actionWarEngineer.distancebase = 0
				return move()
		#si le deuxieme mur n'est as construit
		elif (not actionWarEngineer.deuxiememur):
			#si je ne suis pas a 9 de distance
			if (actionWarEngineer.distancebase != 9):
				actionWarEngineer.distancebase = actionWarEngineer.distancebase + 1
				return move()
			#si je suis a 9 de distance
			elif (actionWarEngineer.distancebase == 9):
				setHeading(getHeading()+ 275)
				actionWarEngineer.deuxiememur = True
				actionWarEngineer.distancebase = 0
				setNextBuildingToBuild(WarAgentType.Wall)
				actionWarEngineer.nextState = SearchFoodState
				return build()

		return move()

class SearchFoodState(object):
	@staticmethod
	def execute():
		setDebugString("SearchFoodState")

		percepts = getPercepts()

		if isBagFull():
			actionWarEngineer.nextState = GoHomeState
			return move()

		actionWarEngineer.nextState = SearchFoodState

		if isBlocked():
			RandomHeading()
			return move()

		#pour tous les messages	
		for msg in getMessages():
			if (msg.getMessage() == "nourriture trouver" and not isBagFull()):
				setHeading(msg.getAngle())
				return move()

		#pour tous se que je voit
		for percept in percepts:
			#si c'est une base
			if (percept.getType().equals(WarAgentType.WarBase)):
				#si c'est une base ennemie
				if (isEnemy(percept)):
					broadcastMessageToAll("Base ennemie trouver", "")
					return move()
				#sinon c'est une base allie et si je suis assez pres pour donner et que mon sac n'est pas vide je donne
				elif (percept.getDistance() < maxDistanceGive() and not isBagEmpty()):
					setHeading(percept.getAngle())
					giveToTarget(percept)
					return give()
				#sinon si je suis pas assez pres
				else:
					#je me rapproche
					if (not isBagFull()):
						setHeading(percept.getAngle())
						return move()
			#si je percoit de la bouf
			if (percept.getType().equals(WarAgentType.WarFood)):
				broadcastMessageToAll("nourriture trouver", "")
				#si je suis asse pres et que mon sac n'est pas plein je prend
				if (percept.getDistance() < getMaxDistanceTakeFood() and not isBagFull()):
					setHeading(percept.getAngle())
					return take()
					#sinon si je suis pas assez pres
				else: 
					#je me rapproche
					if (not isBagFull()):
						setHeading(percept.getAngle())

		return move()

class GoHomeState(object):
	@staticmethod
	def execute():
		setDebugString("GoHomeState")

		percepts = getPercepts()

		if getNbElementsInBag() == 0:

			# Transition vers l'etat SearchFood
			actionWarEngineer.nextState = SearchFoodState
			return move()

			# Maintien de l'etat
		actionWarEngineer.nextState = GoHomeState

		if isBlocked():
			RandomHeading()
			return move()

		#pour tous se que je vois	
		for percept in percepts:
			#si c'est une base
			if (percept.getType().equals(WarAgentType.WarBase)):
				#sinon c'est une base allie et si je suis assez pres pour donner et que mon sac n'est pas vide je donne
				if (percept.getDistance() < maxDistanceGive() and not isBagEmpty()):
					setHeading(percept.getAngle())
					giveToTarget(percept)
					return give()
				#sinon si je suis pas assez pres
				else:
					#je me rapproche
					setHeading(percept.getAngle())
					return move()

		#pour tous les messages	
		for msg in getMessages():
			#si la base fais coucou
			if msg.getMessage() == "Je suis la base":
				setHeading(msg.getAngle())
				return move()

		return move()


class WiggleState(object):
	@staticmethod
	def execute():
		setDebugString("WiggleState")

		if (isBlocked()) :
			RandomHeading()

		return move();

def reflexes():
	if getPerceptsEnemiesWarBase():
		broadcastMessageToAll("Base ennemie trouver", "")
		setDebugString("Base ennemie trouve");
		actionWarEngineer.nextState = SearchFoodState

	return None

def actionWarEngineer():
	result = reflexes() # Reflexes

	if result:
		return result

	# FSM - Changement d'etat
	actionWarEngineer.currentState = actionWarEngineer.nextState
	actionWarEngineer.nextState = None

	if actionWarEngineer.currentState:
		return actionWarEngineer.currentState.execute()
	else:
		result = WiggleState.execute()
		actionWarEngineer.nextState = WiggleState
		return result

# Initialisation des variables
actionWarEngineer.nextState = Mur
actionWarEngineer.currentState = None
actionWarEngineer.base = False
actionWarEngineer.arriver = False
actionWarEngineer.distancebase = 0
actionWarEngineer.premiermur = False
actionWarEngineer.deuxiememur = False