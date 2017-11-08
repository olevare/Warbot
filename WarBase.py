def actionWarBase():
	#Messages
	broadcastMessageToAll("Je suis la base", "");

	percepts = getPercepts()

	#pour tous se que je voit
	for percept in getPerceptsEnemies():
		broadcastMessageToAll("Defence", "");
	
	if (not isBagEmpty() and getHealth() <= 5750):
		return eat();

	if(actionWarBase.debut):
		if getHealth() >= 3000 :
			actionWarBase.compteurlight = actionWarBase.compteurlight + 1
			if(actionWarBase.compteurlight == 12):
				actionWarBase.debut = False
			setNextAgentToCreate(WarAgentType.WarLight)
			return create()

	#pour tous les messages	
	for msg in getMessages():
		#si la base fais coucou
		if msg.getMessage() == "Je suis vivant":
			actionWarBase.compteurvie = actionWarBase.compteurvie + 1

	if(actionWarBase.compteurvie == 0):
		actionWarBase.debut = True

	else:
		if(getHealth() >= 5750):
			if(actionWarBase.compteurlight >= 10):
				broadcastMessageToAll("attaque", "")
				actionWarBase.compteurlight = 0

			actionWarBase.compteurlight = actionWarBase.compteurlight + 1
			setNextAgentToCreate(WarAgentType.WarLight)
			return create()

	return idle()


# Initialisation des variables
actionWarBase.compteurlight = 0
actionWarBase.compteurvie = 0
actionWarBase.debut = True