from classes import *

robot1 = Robot("StandoMech", 120, 20, Speed.medium, SelfRepair(10))
robot2 = Robot("Dendroid", 400, 10, Speed.slow, SelfRepair(5))
robot3 = Robot("SonicNet", 200, 20, Speed.fast, SpeedMalfunction())
robot4 = Robot("AetherBot", 120, 30, Speed.medium, LastUpgrade(1.5))
robot5 = Robot("AstTron", 80, 40, Speed.slow, LastUpgrade(5))
robot6 = Robot("TankAI", 900, 5, Speed.slow, SelfRepair(0))
robot7 = Robot("BadRepairBot", 300, 25, Speed.slow, SelfRepair(-5))
robot8 = Robot("SonicMeta", 240, 18, Speed.fast, SpeedMalfunction())

robotList = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8]
game = Game(robotList, False)

while (not game.exit):
    game.game_page()
