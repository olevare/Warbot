def actionWarTurret():
	#pour tous se que je voit
    for percept in getPerceptsEnemies():
    	broadcastMessageToAll("Defence", "");
        setHeading(percept.getAngle())
        if (isReloaded()):
            return fire()
        else:
            return reloadWeapon()

    setHeading(getHeading()+ 180)
    return idle()