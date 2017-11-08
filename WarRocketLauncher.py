class Attack(object):
	@staticmethod
	def execute():
		setDebugString("Je suis attack")

		percepts = getPercepts()

		actionWarRocketLauncher.nextState = Attack

		if isBlocked():
			RandomHeading()
			return move()

		#pour tous se que je voit
		for percept in percepts:
			#si c'est une base
			if (percept.getType().equals(WarAgentType.WarBase)):
				#si c'est une base ennemie je tire
				if (isEnemy(percept)):
					broadcastMessageToAll("Base ennemie trouver", "")
					setHeading(percept.getAngle())
					setTargetDistance(percept.getDistance())
					if (not isBagEmpty() and getHealth() <= 100):
						return eat();
					elif (isReloaded()):
						return fire()
					else:
						return reloadWeapon()

		for msg in getMessages():
			#si la base ennemie est trouver je fonce
			if msg.getMessage() == "Base ennemie trouver":
				setHeading(msg.getAngle())
				return move()

		actionWarRocketLauncher.nextState = SearchFoodState
		return move()

class Defence(object):
	@staticmethod
	def execute():
		setDebugString("Je suis Defence")

		percepts = getPercepts()

		actionWarRocketLauncher.nextState = SearchFoodState

		if isBlocked():
			RandomHeading()
			return move()

		#pour tous se que je voit
		for percept in percepts:
			if (isEnemy(percept)):
				setHeading(percept.getAngle())
				if (not isBagEmpty() and getHealth() <= 100):
					return eat();
				elif (isReloaded()):
					return fire()
				else:
					return reloadWeapon()

		#pour tous les messages	
		for msg in getMessages():
			#si la base fais coucou
			if msg.getMessage() == "Je suis la base":
				setHeading(msg.getAngle())
				return move()

		return move()

class SearchFoodState(object):
	@staticmethod
	def execute():
		setDebugString("SearchFoodState")

		percepts = getPercepts()

		if isBagFull():
			actionWarRocketLauncher.nextState = GoHomeState
			return move()

		actionWarRocketLauncher.nextState = SearchFoodState

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
					actionWarRocketLauncher.nextState = Attack
					setHeading(percept.getAngle())
					return fire()
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
			actionWarRocketLauncher.nextState = SearchFoodState
			return move()

			# Maintien de l'état
		actionWarRocketLauncher.nextState = GoHomeState

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
		actionWarRocketLauncher.nextState = Attack

	#pour tous les messages	
	for msg in getMessages():
		if msg.getMessage() == "Base ennemie trouver":
			setHeading(msg.getAngle())
			actionWarRocketLauncher.nextState = Attack

	#pour tous les messages	
	for msg in getMessages():
		if msg.getMessage() == "Defence":
			setHeading(msg.getAngle())
			actionWarRocketLauncher.nextState = Defence

	return None

def actionWarRocketLauncher():
	result = reflexes() # Reflexes

	if result:
		return result

	# FSM - Changement d'état
	actionWarRocketLauncher.currentState = actionWarRocketLauncher.nextState
	actionWarRocketLauncher.nextState = None

	if actionWarRocketLauncher.currentState:
		return actionWarRocketLauncher.currentState.execute()
	else:
		result = WiggleState.execute()
		actionWarRocketLauncher.nextState = WiggleState
		return result

# Initialisation des variables
actionWarRocketLauncher.nextState = SearchFoodState
actionWarRocketLauncher.currentState = None