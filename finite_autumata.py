"""
Finite automata
"""
import random

class StateQueue:
    def __init__(self, states=None) -> None:
        self.states = states or []

    def __len__(self):
        return len(self.states)

    def add_state(self, state=None):
        if not state:
            if len(self.states) < 7:
                self.states.append('Sleep')
            elif len(self.states) in [7, 8, 14, 16, 19, 20, 21, 22] and self.states[-2] != 'Eat':
                self.states.append('Eat')
                self.states.append('Code')
            elif len(self.states) in range (18, 21) and self.states[-1] == 'Code':
                self.states.append('Pray')
                self.states.append('Relax')
            else:
                self.states.append('Code')
        else:
            self.states.append(state)

    def clear(self):
        self.states = []
    
    def popleft(self):
        return self.states.pop(0)
    
    def insert(self, state):
        self.states.insert(0, state)

class LifeAutomata:
    """
    This class represents a simulation of an automata's life throughout a day.
    """
    def __init__(self):
        """
        Initializes the Lifeautomata object with default values for its attributes.
        """
        self.energy = 0
        self.hapiness = 0
        self.name = 'Sleep'
        self.hour = 0
        self.state_handler = States()
        self.queue = StateQueue(['Sleep'])

    @staticmethod
    def formatted_time(time):
        """
        Converts a decimal representation of time into a formatted string 
        representing hours and minutes.
        """
        hours, minutes = divmod(time, 1)
        if hours >= 24:
            hours -= 24
        return f"{int(hours)}:{int(minutes*60):02d}"

    def simulate_day(self):
        """
        Simulates a day in the life of the automata, updating its state, 
        energy, and happiness over time.
        """
        while len(self.queue) < 32:
            if len(self.queue) < 8:
                self.queue.add_state('Sleep')
            elif random.random() < 0.03:
                self.queue.add_state('Depression')
            elif random.random() < 0.07:
                self.queue.add_state('Op')
            elif random.random() < 0.1:
                self.queue.add_state('Dog')
            else:
                self.queue.add_state()
        while self.queue:
            started_time = self.hour
            if self.name != 'Sleep' and (self.hapiness < 30 or self.energy < 30):
                self.queue.insert('Eat')
            next_activity = self.queue.popleft()
            self.name = next_activity
            self.state_handler.handle_state(self)

            self.hapiness = max(0, self.hapiness)
            self.energy = max(0, self.energy)
            print(f"Start time: {self.formatted_time(started_time)}, end time \
{self.formatted_time(self.hour)}, happiness: {self.hapiness}, energy: {self.energy}")
            print()

        self.energy = 0
        self.hapiness = 0
        self.name = 'Sleep'
        self.hour = 7
        print('The end of the day. It is time to sleep.')



class States:
    """
    This class handles different states of the automata.
    """
    def handle_state(self, automata):
        """
        Handles the current state of the automata and delegates 
        the execution to specific state methods.
        """
        if automata.name == 'Sleep':
            self.sleep(automata)
        elif automata.name == 'Eat':
            self.eat(automata)
        elif automata.name == 'Code':
            self.code(automata)
        elif automata.name == 'Pray':
            self.pray(automata)
        elif automata.name == 'Relax':
            self.relax(automata)
        elif automata.name == 'Depression':
            self.depression(automata)
        elif automata.name == 'Dog':
            self.dog(automata)
        elif automata.name == 'Op':
            self.op_correction(automata)

    @staticmethod
    def sleep(automata):
        """
        Handles the sleep state of the automata, updating its attributes accordingly.
        """
        if automata.hour == 7:
            print('Ohhh, one more beautiful day before discrete math талон :)', end=' ')
            automata.hapiness += random.randint(30, 50)
            automata.energy += random.randint(30, 50)
            automata.name = 'Eat'
            automata.hour += 0.25
        else:
            print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz................', end=' ')
            automata.hour += 1

    @staticmethod
    def eat(automata):
        """
        Handles the eat state of the automata, updating 
        its attributes and printing eating messages.
        """
        dinner = False
        lunch = False
        automata.hapiness += random.randint(50, 90)
        automata.energy += random.randint(50, 90)
        automata.name = 'Code'
        if int(automata.hour) in range(7, 8):
            print('Yummy breakfast', end=' ')
        elif int(automata.hour) in range(14, 16):
            print('Трапезна my beloved', end=' ')
        elif int(automata.hour) in range(19, 22) and not dinner:
            dinner = True
            if not lunch:
                print('I do not have a lunch, so I need to eat more now.')
            else:
                print("It's time for dinner.", end=' ')
        else:
            print('I am growing so I need to eat a lot.', end=' ')
        automata.hour += 0.5

    @staticmethod
    def code(automata):
        """
        Handles the code state of the automata, updating 
        its attributes and transitioning to other states.
        """
        if int(automata.hour) in range(7, 13):
            print('Oh coding! Here I go again', end=' ')
            automata.hour += 1
        elif int(automata.hour) in range(13, 19):
            print("Klatz, klatz, I'm a programmer.", end=' ')
            if int(automata.hour) in range(13, 14):
                automata.name = 'Eat'
            else:
                automata.name = 'Code'
            automata.hour += 1
        else:
            print("I am a depressed debuger :(", end=' ')
            automata.hapiness -= random.randint(50, 90)
            automata.energy -= random.randint(50, 90)
            if int(automata.hour) in range(18, 21):
                automata.name = 'Eat'
            else:
                automata.name = 'Pray'
            automata.hour += 1

    @staticmethod
    def pray(automata):
        """
        Handles the pray state of the automata, updating 
        its attributes and transitioning to the relax state.
        """
        automata.hour += 0.25
        automata.hapiness += 1000
        automata.name = 'Relax'
        print("'Three times the Ave Maria and go on.'ⓒ Stepan Fedyniak", end=' ')

    @staticmethod
    def relax(automata):
        """
        Handles the relax state of the automata, updating its attributes 
        and transitioning back to the code state.
        """
        automata.hour += 1
        automata.hapiness += random.randint(50, 90)
        automata.energy += random.randint(50, 90)
        automata.name = 'Code'
        print('Relaxation', end=' ')


    @staticmethod
    def depression(automata):
        """
        Simulates the automata experiencing depression, affecting its energy and happiness levels.
        """
        automata.hour += 0.25
        automata.hapiness -= random.randint(100, 1000)
        automata.energy -= random.randint(100, 1000)
        print("Oh I have only 30 points 2 weeks before discrete math's exam :(", end=' ')
        automata.name = 'Pray'

    @staticmethod
    def dog(automata):
        """
        Simulates the automata interacting with its dog, boosting its energy and happiness levels.
        """
        automata.hour += 0.25
        automata.hapiness += random.randint(1000, 10000)
        automata.energy += random.randint(1000, 10000)
        print("My dog is such a cutie!", end=' ')
        automata.name = 'Relax'

    @staticmethod
    def op_correction(automata):
        """
        Simulates the automata receiving an operation correction, 
        affecting its energy and happiness levels.
        """
        automata.hour += 1
        automata.hapiness -= random.randint(100, 1000)
        automata.energy -= random.randint(100, 1000)
        print("Pani Tetiana made a correction and gave only 1 day to correct code :(", end=' ')
        automata.name = 'Code'

simulation = LifeAutomata()
simulation.simulate_day()
