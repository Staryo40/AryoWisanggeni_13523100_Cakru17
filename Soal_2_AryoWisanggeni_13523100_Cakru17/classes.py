from enum import Enum
import random
import os
import time

# Robot's passive abilities
class PassiveAbility():
    def apply(self, robot):
        pass

class SelfRepair(PassiveAbility):
    def __init__(self, regenAmount):
        self.regenAmount = regenAmount
    
    def apply(self, robot):
        if (self.regenAmount == 0):
            pass
        elif (self.regenAmount < 0):
            robot.healthPoint += self.regenAmount
            print(f"{robot.name} has hurt itself for {self.regenAmount} hp!")
        else: 
            if (robot.healthPoint + self.regenAmount < robot.maxHP and robot.healthPoint > 0):
                robot.healthPoint += self.regenAmount
                print(f"{robot.name} has regained {self.regenAmount} hp!")
            elif (robot.healthPoint + self.regenAmount >= robot.maxHP):
                robot.healthPoint = robot.maxHP
                print(f"{robot.name} has regained to max hp!")

class SpeedMalfunction(PassiveAbility):
    def apply(self, robot):
        robot.speed = random.choice(list(Speed))
        print(f"{robot.name} has changed its speed to {robot.speed.name}!")

class LastUpgrade(PassiveAbility):
    def __init__(self, attackMultiplier):
        self.active = True
        self.attackMultiplier = attackMultiplier

    def apply(self, robot):
        if (robot.healthPoint <= 0.5 * robot.maxHP and self.active):
            robot.attackPower = robot.attackPower * self.attackMultiplier
            self.active = False
            print(f"{robot.name} unleashed it's final upgrade to increase it's attack!")

# Robot's speed categories
class Speed(Enum):
    slow = 1
    medium = 2
    fast = 3

# Robot class
class Robot:
    def __init__(self, name, maxHP, attackPower, speed: Speed, passive=None):
        self.name = name
        self.maxHP = maxHP 
        self.healthPoint = maxHP
        self.defaultAttack = attackPower
        self.attackPower = attackPower
        self.defaultSpeed = speed
        self.speed = speed
        self.passive = passive
    
    def applyPassive(self):
        if self.passive:
            self.passive.apply(self)

    def reset(self):
        self.healthPoint = self.maxHP
        self.attackPower = self.defaultAttack
        self.speed = self.defaultSpeed
        if (type(self.passive).__name__ == "LastUpgrade"):
            self.passive.active = True

class Battle:
    def __init__(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2

    def crit(self, name):
        rand = random.randint(1,100)
        if (rand <= 10):
            print(f"{name} landed a crit!")
            return 1.25
        else:
            return 1
    
    def draw_hp_bar(self, name, current_hp, max_hp, width=20):
        current_hp = float(current_hp)
        max_hp = float(max_hp)

        hp_ratio = current_hp / max_hp
        hp_length = int(hp_ratio * width)
        
        hp_bar = '[' + '█' * hp_length + ' ' * (width - hp_length) + ']'
        
        print(f"{name} HP: {current_hp}/{max_hp} {hp_bar}")
    
    def start_fight(self):
        robotOne = self.robot1
        robotTwo = self.robot2
        i = 1
        while robotOne.healthPoint > 0 and robotTwo.healthPoint > 0:
            # determine who is the first attacker for the turn
            if robotOne.speed == robotTwo.speed:
                first_attacker = random.choice([robotOne, robotTwo])
            else:
                first_attacker = robotOne if robotOne.speed.value > robotTwo.speed.value else robotTwo

            print(f"\033[1mTURN {i}\033[0m")
            # Both robots attack based on speed
            if first_attacker == robotOne:
                # robotOne attacks first
                damage = robotOne.attackPower * self.crit(robotOne.name)
                robotTwo.healthPoint -= damage
                print(f"{robotOne.name} attacks {robotTwo.name} for {damage} damage!")

                # check if robotTwo is down
                if robotTwo.healthPoint <= 0:
                    print(f"{robotTwo.name} has been defeated!")
                    print(f"{robotOne.name} won!")
                    break

                # robotTwo attacks second
                damage = robotTwo.attackPower * self.crit(robotTwo.name)
                robotOne.healthPoint -= damage
                print(f"{robotTwo.name} attacks {robotOne.name} for {damage} damage!")
            else:
                # robotTwo attacks first
                damage = robotTwo.attackPower * self.crit(robotTwo.name)
                robotOne.healthPoint -= damage
                print(f"{robotTwo.name} attacks {robotOne.name} for {damage} damage!")

                # check if robotOne is down
                if robotOne.healthPoint <= 0:
                    print(f"{robotOne.name} has been defeated!")
                    print(f"{robotTwo.name} won!")
                    break
                
                # robotOne attacks second
                damage = robotOne.attackPower * self.crit(robotOne.name)
                robotTwo.healthPoint -= damage
                print(f"{robotOne.name} attacks {robotTwo.name} for {damage} damage!")

            # Last check if a robot has already defeated
            if robotOne.healthPoint <= 0:
                print(f"{robotOne.name} has been defeated!")
                print(f"{robotTwo.name} won!")
                break
            if robotTwo.healthPoint <= 0:
                print(f"{robotTwo.name} has been defeated!")
                print(f"{robotOne.name} won!")
                break
            
            # Both robots activate their passives
            robotOne.applyPassive()
            robotTwo.applyPassive()
            i += 1
            print("")
            self.draw_hp_bar(robotOne.name, robotOne.healthPoint, robotOne.maxHP)
            self.draw_hp_bar(robotTwo.name, robotTwo.healthPoint, robotTwo.maxHP)
            print("")
            time.sleep(0.2)

        robotOne.reset()
        robotTwo.reset()
        print("")

        out = input("Press enter to go back to main page.")

class Game:
    def __init__(self, robotList, exit):
        self.robotList = robotList
        self.exit = exit

    def print_robot_list(self):
        print("Robot List:")
        i = 1
        for robot in self.robotList:
            print(f"{i}. {robot.name}")
            i += 1

    def show_robots(self):
        self.print_robot_list()
        print("Type in the robot's index to show it's stat")
        robotSelection = int(input(f"Robot index (1-{len(self.robotList)}): "))
        print("")
        robotID = robotSelection-1
        print(f"Robot name: {self.robotList[robotID].name}")
        print(f"Robot max HP: {self.robotList[robotID].maxHP}")
        print(f"Robot attack power: {self.robotList[robotID].attackPower}")
        print(f"Robot speed: {self.robotList[robotID].speed.name}")
        passive = type(self.robotList[robotID].passive).__name__
        passiveReal = self.robotList[robotID].passive
        if (passive == "SelfRepair"):
            print(f"Robot passive: Self Repair ({passiveReal.regenAmount})")
        if (passive == "SpeedMalfunction"):
            print(f"Robot passive: Speed Malfunction")
        if (passive == "LastUpgrade"):
            print(f"Robot passive: Last Upgrade ({passiveReal.attackMultiplier})")
        print("")

        out = input("Press enter to go back to main page.")


    def add_robot(self):
        self.print_robot_list()
        print("")
        newName = input("Enter new robot's name: ")
        newMaxHP = int(input("Enter new robot's max HP: "))
        newAttackPower = int(input("Enter new robot's attack power: "))

        inputSpeed = input("Enter new robot's speed (slow, medium, or fast): ")
        while inputSpeed not in ["slow", "medium", "fast"]:
            inputSpeed = input("Enter a VALID speed (slow, medium, or fast): ")

        if (inputSpeed == "slow"):
            newSpeed = Speed.slow
        if (inputSpeed == "medium"):
            newSpeed = Speed.medium
        if (inputSpeed == "fast"):
            newSpeed = Speed.fast

        newPassive = input("Enter new robot's passive ('self repair', 'speed malfunction', or 'last upgrade'): ")
        while newPassive not in ["self repair", "speed malfunction", "last upgrade"]:
            newPassive= input("Enter a VALID passive ('self repair', 'speed malfunction', or 'last upgrade'): ")

        if (newPassive == "self repair"):
            repair_value = int(input("Enter repair value: "))
            newRobot = Robot(newName, newMaxHP, newAttackPower, newSpeed, SelfRepair(repair_value))
        if (newPassive == "speed malfunction"):
            newRobot = Robot(newName, newMaxHP, newAttackPower, newSpeed, SpeedMalfunction())
        if (newPassive == "last upgrade"):
            attack_multi = int(input("Enter attack multiplication value: "))
            newRobot = Robot(newName, newMaxHP, newAttackPower, newSpeed, LastUpgrade(attack_multi))

        self.robotList.append(newRobot)
        print("")

        out = input("Press enter to go back to main page.")

    def start_game(self):
        print("It's time to DUEL!")
        self.print_robot_list()
        robot1 = int(input(f"Pick the first robot (1-{len(self.robotList)}): "))
        robot2 = int(input(f"Pick the second robot (1-{len(self.robotList)}): "))
        battle = Battle(self.robotList[robot1-1], self.robotList[robot2-1])
        os.system('cls' if os.name == 'nt' else 'clear')
        battle.start_fight()
       
    def game_page(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the game of fighting robots!")
        print("1. Start Battle")
        print("2. View Robots")
        print("3. Add Robot")
        print("4. Exit")
        selection = int(input("Enter input by index (1-4): "))
        while (selection <= 0 or selection > 4):
            selection = int(input("Enter VALID input (1-3): "))
        os.system('cls' if os.name == 'nt' else 'clear')
        if (selection == 1):
            self.start_game()
        if (selection == 2):
            self.show_robots()
        if (selection == 3):
            self.add_robot()
        if (selection == 4):
            self.exit = True