class Attack(object):
	@staticmethod
	def execute():
		setDebugString("Je suis attack")

		percepts = getPercepts()

		actionWarExplorer.nextState = Attack

		if isBlocked():
			RandomHeading()
			return move()

		for msg in getMessages():
			#si la base ennemie est trouver je fonce
			if msg.getMessage() == "Base ennemie trouver":
				actionWarExplorer.nextState = SearchFoodState
				return move()

		#pour tous se que je voit
		for percept in percepts:
			#si c'est une base
			if(percept.getType().equals(WarAgentType.WarBase)):
				#si c'est une base ennemie je tire
				if(isEnemy(percept)):
					broadcastMessageToAll("Base ennemie trouver", "")
					actionWarExplorer.nextState = SearchFoodState
					return move()

		return move()

class SearchFoodState(object):
	@staticmethod
	def execute():
		setDebugString("SearchFoodState")

		percepts = getPercepts()

		if isBagFull():
			actionWarExplorer.nextState = GoHomeState
			return move()

		actionWarExplorer.nextState = SearchFoodState

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
			# Transition vers l'état SearchFood
			actionWarExplorer.nextState = SearchFoodState
			return move()

			# Maintien de l'état
		actionWarExplorer.nextState = GoHomeState

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
		setDebugString("Base ennemie trouvé");
		actionWarExplorer.nextState = SearchFoodState

	#pour tous les messages	
	for msg in getMessages():
		if msg.getMessage() == "attaque":
			actionWarExplorer.nextState = Attack

	return None

def actionWarExplorer():
	result = reflexes() # Reflexes

	if result:
		return result

	# FSM - Changement d'état
	actionWarExplorer.currentState = actionWarExplorer.nextState
	actionWarExplorer.nextState = None

	if actionWarExplorer.currentState:
		return actionWarExplorer.currentState.execute()
	else:
		result = WiggleState.execute()
		actionWarExplorer.nextState = WiggleState
		return result

# Initialisation des variables
actionWarExplorer.nextState = SearchFoodState
actionWarExplorer.currentState = None