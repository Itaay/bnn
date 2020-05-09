from brain.synapse import *
ID = 0
EPSIL = 0.01
RECURSION_LIMIT = 10


def get_id():
    global ID
    tmp = ID
    ID += 1
    return tmp


class Neuron:
    def __init__(self, location, color =(255,0,0)):

        self.id = get_id()  # id of neuron
        self.location = location    # location of neuron
        self.axons = []   # list of all axons the neuron has  (output connections)
        self.dendrites = [] # list of all dendrites the neuron has (input connections)
        self.memory = 0.0   # memory state of neuron(if untouched for a while, state will return to memory state)
        self.score = 0.0    # concentration of "dopamine": dilutes over time
        self.state = 0.0
        self.decay = 0.5
        self.charge_cap = 10.0

        self.charge_noise = 0.05

        self.threshold = 0.3
        self.original_threshold = self.threshold
        self.threshold_decay = 0.1
        self.minimum_threshold = 0.01
        self.max_threshold = 10.0

        self.feedback_speed = 3.0
        self.der_sign = 1.0
        self.peak = self.threshold * 2



        self.average_charge = 0.0
        self.avg_decay = 0.7
        self.accumulated_charge = 0.0

        self.in_loop = False

        self.reward_distribute_threshold = 0.01

        self.can_learn = True

        self.color = color

    def distance(self, b):
        """
        return the euclidian distance between this neuron and the given one
        :param b: Another neuron
        :return:
        """
        return np.sqrt(np.sum((self.location-b.location)**2))

    def update(self):
        """
        Update the neuron.
        Steps:
        -Transmit charge through the synapses
        -Degrade state back to memory(with certain step size, we will call decay)
        :return:
        """

        #   self.threshold = 0.5*self.original_threshold + 0.5*self.threshold

        self.create_charge_noise()

        self.handle_firing()
        """if self.ready_to_fire():
            self.fire_signals(self.state-self.threshold)"""
        self.charge_decay()
        self.cap_charge()
        self.update_avg_charge()

        if self.can_learn:
            self.adjust_threshold()

    def handle_firing(self):
        if self.state > self.threshold:
            if self.der_sign == 1:
                self.state *= self.feedback_speed
            else:
                amount_to_dispose = self.state / max(1.0, self.feedback_speed)
                self.fire_signals(amount_to_dispose)
        elif self.state <= self.threshold:
            self.state = (1-self.decay)*self.memory + (self.decay * self.state)
        if self.state >= self.peak:
            self.der_sign = -1
        if self.state <= self.threshold:
            self.der_sign = 1

    def adjust_threshold(self):
        if self.average_charge > self.threshold:
            self.add_to_threshold(self.average_charge)
        self.threshold = self.original_threshold*(1-self.threshold_decay) + self.threshold*self.threshold_decay
        self.charge_noise = self.threshold

    def add_to_threshold(self, addition):
        self.threshold = max(min((np.tanh(addition) * self.threshold) + self.threshold - self.memory, self.max_threshold),self.minimum_threshold)

    def search_opposite_synapse(self, d):
        """
        Given a dendrite instance, find the axon of the opposite path
        :param d:
        :return:
        """
        for a in self.axons:
            if a.end_point == d.start_point:
                return a
        return None

    def update_avg_charge(self):
        self.average_charge = (self.avg_decay * sum([s.activity for s in self.dendrites])) + (1-self.avg_decay)*(self.average_charge)
        #   self.average_charge = self.avg_decay * self.accumulated_charge + (1.0-self.avg_decay)*(self.average_charge)


    def cap_charge(self):
        self.state = min(max(-self.charge_cap, self.state), self.charge_cap)


    def create_charge_noise(self):
        noise = (np.random.random() * 2 * self.charge_noise) - self.charge_noise
        self.state += noise
        self.accumulated_charge += noise
        self.cap_charge()

    def ready_to_fire(self):
        """
        If the difference in pottential relative to the neutral state is above the threshold,
        ready to fire
        :return:
        """
        if self.state-self.memory > self.threshold:
            return True

    def charge_buildup(self):
        """
        Once above the threshold, the charge inside the cell causes a feedback loop which increases even more
        The charge inside.
        :return:
        """
        alpha = 1.0
        self.state += alpha*(self.state - self.memory)
        self.cap_charge()

    def fire_signals(self, charge_to_release):
        """
        Handle the firing of the signals( and therefore release of charge)
        :return:
        """

        total_strength = sum([c.strength for c in self.axons])
        if total_strength == 0:
            return
        charge_released = 0.0
        for a in sorted(self.axons, key=lambda b: b.strength, reverse=True):
            percentage = a.strength / total_strength
            disperesed = a.fire(charge_to_release*percentage)
            charge_to_release -= disperesed
            charge_released += disperesed
            total_strength -= a.strength
        self.state -= charge_released
        self.accumulated_charge -= charge_released
        return charge_released

    def charge_decay(self):
        """
        Decay the charge of the neuron back to it's neutral state, by doing a moving average decay
        :return:
        """
        self.state = (self.decay*self.memory)+((1-self.decay)*self.state)

    def absorb(self, charge):
        self.state += charge.q
        charge.v = 0.0
        self.accumulated_charge += charge.q
        self.cap_charge()

    def connect(self, b, starter_strength):
        """
        Connect to another neuron b(self ----------> b)
        :param b:
        :param starter_strength:
        :return:
        """
        new_axon = Synapse(self, b, starter_strength)
        self.axons.append(new_axon)
        b.dendrites.append(new_axon)

    def reward(self, amount, depth=0):
        """
        Handle the rewarding system of the cell
        :param amount: reward given: Non Negative value
        :return:
        """
        if not self.can_learn:
            return
        transaction_friction = 1.0
        if abs(amount) < EPSIL:
            return
        sign = amount / abs(amount) # the if statement above prevents division by zero amongst other things
        abs_amount = abs(amount)
        if depth > RECURSION_LIMIT:
            self.add_to_threshold(-amount)
            self.score += amount
            return
        else:
            to_self = sign * min(abs_amount, self.reward_distribute_threshold)
            self.add_to_threshold(max(0.0, -to_self))
            self.score += to_self
        amount -= to_self
        if amount != 0:
            # Get sum of activities of all dendrites
            total_input_activity = sum([d.strain for d in self.dendrites])
            counter = 0
            for d in sorted(self.dendrites, key=lambda b: b.strain, reverse=True):    # iterate over all dendrites
                if total_input_activity != 0.0:
                    frac = d.strain / total_input_activity  # calculate relative contribution to input activity
                    reward_away_size = amount * frac
                    reward_away_size = transaction_friction * reward_away_size
                    amount -= reward_away_size  # remove from total reward pool
                    total_input_activity -= d.strain  # remove activity from activity sum
                    if counter >= 3:
                        reward_away_size *= -1.0
                        reward_away_size = min(reward_away_size, 0.0)
                    d.reinforce(reward_away_size, depth=depth+1)
                    ax = self.search_opposite_synapse(d)
                    if ax is not None:
                        ax.set_strength(ax.strength + min(reward_away_size*0.1, 0.0))
                        ax.cap_strength()

                counter += 1

    def draw(self, screen):
        for a in self.axons:
            a.draw(screen)
        color = [min(50, c) + c * self.average_charge for c in self.color]
        color = clip_color(color)
        pygame.draw.circle(screen, color, np.array(self.location, dtype=int), 10)

    def set_learning_state(self, state):
        self.can_learn = state
        for a in self.axons:
            a.set_learning_state(state)

    def feed_charge(self, charge):
        self.state = charge
        self.cap_charge()







