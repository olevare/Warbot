def actionWarKamikaze():
    if (actionWarKamikaze.attack):
        if isBlocked():
            RandomHeading()
            return move()

        #pour tous se que je voit
        for percept in getPercepts():
            #si c'est une base
            if (percept.getType().equals(WarAgentType.WarBase)):
                #si c'est une base ennemie je fonce
                if (isEnemy(percept)):
                    broadcastMessageToAll("Base ennemie trouver", "")
                    setHeading(percept.getAngle())
                    return fire()
        return move()
    else:
        #pour tous les messages
        for msg in getMessages():
            #si la base ennemie est trouver je fonce
            if msg.getMessage() == "Base ennemie trouver":
                actionWarKamikaze.attack = True
                setHeading(msg.getAngle())
                return move()
    return idle()

# Initialisation des variables
actionWarKamikaze.attack = False