from brain.neuron import *
from utils import *
from brain.charge import *
from brain.space import *
import pygame
import time
SCREEN_SIZE = (800, 800)
BACKGROUND_COLOR = (150,150,170)
TITLE = 'snn simulation'
#   np.random.seed(101080)

FLOPPER = 750


class Colony:
    def __init__(self):
        self.cells = []
        self.name = None
        self.parents = []
        self.children = []
        self.starter_strength = 0.1

    def update(self, turns=range(1)):
        if type(turns) == int:
            turns = range(turns)
        for i in turns:  # for each simulation epoch
            """if i == 3000:
                self.set_learning_state(False)
                input()"""

            """self.reward(i)
            if (i//FLOPPER) % 2 == 0:
                for s in range(min(len(self.cells), 2)):
                    self.cells[s].state = 1.0
            else:
                for s in range(2, min(len(self.cells), 4)):
                    self.cells[s].state = 1.0
            """
            for c in self.cells:    # first, go over all cells
                for a in c.axons:   # and for each one of them, iterate over it's axons(output connections)
                    a.update()  # update them
            for c in self.cells:    # then iterate over all the cells again, and this time update the cells themselves
                c.update()
            """supposed = -1 - (i // FLOPPER) % 2
            diff = self.cells[-1].average_charge - self.cells[-2].average_charge
            conn = self.connection_between_ids(2, 9)
            #   print("iteration: " + str(i) +", strength: " + str(conn.strength) + ", strain: " + str(conn.strain) + ", activity: " + str(conn.activity) + ", current_charge: " + str(conn.current_activity()) )
            #print(diff)"""
            """if supposed == -1:
                supposed = -2
            else:
                supposed = -1
            """
            """
            if supposed == -1:
                print(str(diff))
            else:
                print(str(-diff))"""
            #   print(self.cells[-2].average_charge)
            #   print(self.cells[supposed].average_charge)
            #   print(self.cells[-1].state)
            #   print(self.cells[-2].average_charge)
            #   print(self.cells_thresholds()[-2:])

            #   print(self.score())
            #   print(self.cells[-1].average_charge)
            #   print(min([c.state for c in self.cells]))



    def reward(self, i):

        if (i // FLOPPER) % 2 == 0:
            self.cells[-1].reward(self.cells[-1].average_charge)
            self.cells[-2].reward(min(0, -self.cells[-2].average_charge))
        else:
            self.cells[-1].reward(min(0, -self.cells[-1].average_charge))
            self.cells[-2].reward(self.cells[-2].average_charge)
            #   self.cells[-2].reward(self.cells[-2].average_charge)
            #   self.cells[-1].reward(-self.cells[-2].average_charge)
        #   self.cells[-1].reward(relation)

    def breed(self):
        pass

    def connect_nearest_neighbors(self, max_neighbors):
        for c in self.cells:
            neighbors = search_closest(c, self.cells, n=min(len(self.cells)-1, max_neighbors))
            for n in neighbors:
                c.connect(n, self.starter_strength)

    def score(self):
        return sum([c.score for c in self.cells])

    def draw(self, screen):
        for i in range(len(self.cells)):
            self.cells[i].draw(screen)

    def most_activated_cell(self):
        res = np.argmax([c.state for c in self.cells])
        return res

    def most_activated_cells(self):
        res = sorted(range(len(self.cells)), key=lambda a:self.cells[a].score, reverse=True)
        return res

    def print_locations_of_cells(self):
        print([c.location for c in self.cells])

    def cells_thresholds(self):
        return [c.threshold for c in self.cells]

    def charge_count(self):
        counter = 0
        for c in self.cells:
            for a in c.axons:
                counter += len(a.signals)
        return counter

    def set_learning_state(self, state):
        for c in self.cells:
            c.set_learning_state(state)

    def connection_between_ids(self, a, b):
        if self.cells[a].id == a:
            start_point = self.cells[a]
        else:
            start_point = None
            for i in range(len(self.cells)):
                if self.cells[i].id == a:
                    start_point = self.cells[i]
        for a in start_point.axons:
            if a.end_point.id == b:
                return a



def generate(n, volume, max_neighbors):
    brain = Colony()
    for i in range(n):
        new_cell = Neuron(volume.random_loc(), (255, 0, 0))
        brain.cells.append(new_cell)
    brain.connect_nearest_neighbors(max_neighbors)
    return brain


def simulate(brain):
    screen_size = SCREEN_SIZE
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    if TITLE is not None:
        pygame.display.set_caption(TITLE)

    done = False
    fps = 10000
    brain.draw(screen)
    pygame.display.flip()
    i = 0
    while not done:
        """if i % FLOPPER == 0:
            if (i // FLOPPER) % 2 == 0:
                print("flip: Green")
            else:
                print("flip: Yellow")"""
        start = time.time()
        screen.fill(BACKGROUND_COLOR)
        #   clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    fps += 1
                if event.button == 5:
                    fps = max(0, fps - 1)
        brain.update(range(i, i+1))
        brain.draw(screen)
        i += 1

        pygame.display.flip()
        #   print(str(time.time()-start) + ", charge counter: " + str(brain.charge_count()))


def default_generate(n, max_neighbors=10, volume=None):
    if volume is None:
        volume = Volume(shape='rect', location=np.array([0, 0, 0]), size=np.array([300, 300]))
    return generate(n, volume, max_neighbors)





#   environment = Volume(shape='rect', location=np.array([0, 0, 0]), size=np.array([800, 800]))
#   br = generate(100, environment, 10)
#   simulate(br)
#   br.update(3000)
