"""A simulator for Zombie Apocalypse.

(see Munz et al. 2009)
http://mysite.science.uottawa.ca/rsmith43/Zombies.pdf
"""

import os

# Set this before import matplotlib
os.environ['MPLCONFIGDIR'] = '/tmp'

# This is needed before importing pyplot for rendering the image
import matplotlib
matplotlib.use('Agg')

import numpy
from matplotlib import pyplot
from scipy.integrate import odeint


DEFAULT_TIME_VECTOR = numpy.linspace(0, 5., 1000)
DEFAULT_INITIAL_POPULATION = 500.
DEFAULT_INITIAL_ZOMBIE_POPULATION = 0.
DEFAULT_INITIAL_DEATH_POPULATION = 0.
DEFAULT_BIRTH_RATE = 0.       # birth rate
DEFAULT_NATURAL_DEATH_PERCENT = 0.01  # natural death percent (per day)
DEFAULT_TRANSMISSION_PERCENT = 0.95  # transmission percent  (per day)
DEFAULT_RESURRECT_PERCENT = 0.01  # resurrect percent (per day)
DEFAULT_DESTROY_PERCENT = 0.01  # destroy percent  (per day)
PLOT_TITLE_TEMPLATE = """\
init po: {}, init zombie: {}, init death: {}, {} daily birth
death pct. {}%, trans pct. {}%, resur pct. {}%, destroy pct. {}%."""


class ZombieApocalypseSimulator(object):
    """A simulator for Zombie Apocalypse (see Munz et al. 2009)."""

    def __init__(self,
                 time_vector=DEFAULT_TIME_VECTOR,
                 initial_population=DEFAULT_INITIAL_POPULATION,
                 initial_zombie_population=DEFAULT_INITIAL_ZOMBIE_POPULATION,
                 initial_death_population=DEFAULT_INITIAL_DEATH_POPULATION,
                 birth_rate=DEFAULT_BIRTH_RATE,
                 natural_death_percent=DEFAULT_NATURAL_DEATH_PERCENT,
                 transmission_percent=DEFAULT_TRANSMISSION_PERCENT,
                 resurrect_percent=DEFAULT_RESURRECT_PERCENT,
                 destroy_percent=DEFAULT_DESTROY_PERCENT):
        """A constructor for the simulator.

        Args:
            time_vector: A time span for the simulation.
            initial_population: Initial population of the human beings.
            initial_zombie_population: Initial population of the Zombies.
            initial_death_population: Initial number of the dead bodies.
            birth_rate: Number of births/day.
            natural_death_percent: Natural death percent per day.
            transmission_percent: Transmission percent per day
                (a human becomes a zombie).
            resurrect_percent: Resurrection percent per day
                (a dead body becomes a zombie).
            destroy_percent: Destroy percent per day
                (a zombie is completely destroyed).
        """
        self.time_vector = time_vector
        self.initial_population = initial_population
        self.initial_zombie_population = initial_zombie_population
        self.initial_death_population = initial_death_population
        self.birth_rate = birth_rate
        self.natural_death_rate = natural_death_percent / 100
        self.transmission_rate = transmission_percent / 100
        self.resurrect_rate = resurrect_percent / 100
        self.destroy_rate = destroy_percent / 100

    def _compute_populations(self, y, t):
        """Compute the populations at the given time point.

        Args: 
            y: A list containing the numbers of human beings, zombies,
               and dead bodies.
            t: A time point for the computation.

        Returns:
            A list containing the numbers of human beings, zombies,
            and dead bodies for the given time point.
        """
        Si = y[0]
        Zi = y[1]
        Ri = y[2]
        # the model equations (see Munz et al. 2009)
        f0 = (self.birth_rate - self.transmission_rate * Si * Zi
              - self.natural_death_rate * Si)
        f1 = (self.transmission_rate * Si * Zi
              + self.resurrect_rate * Ri
              - self.destroy_rate / 100 * Si * Zi)
        f2 = (self.natural_death_rate * Si + self.destroy_rate * Si * Zi
              - self.resurrect_rate * Ri)
        return [f0, f1, f2]

    def _solve(self):
        """Returns the simulated result."""
        y0 = [self.initial_population, self.initial_zombie_population,
              self.initial_death_population]
        return odeint(self._compute_populations, y0, self.time_vector)

    @property
    def plot_title(self):
        """Creates a title string of the result image.

        Returns:
            A title string of the image.
        """
        return PLOT_TITLE_TEMPLATE.format(
            self.initial_population,
            self.initial_zombie_population,
            self.initial_death_population,
            self.birth_rate,
            self.natural_death_rate*100.0,
            self.transmission_rate*100.0,
            self.resurrect_rate*100.0,
            self.destroy_rate*100.0)

    def plot(self, file_object):
        """Creates a png object and write it to the given object.

        Args:
            file_object: A file object for writing the binary data
                of the generated png file.
        """
        soln = self._solve()
        S = soln[:, 0]
        Z = soln[:, 1]
        R = soln[:, 2]
        pyplot.figure()
        pyplot.plot(self.time_vector, S, label='Living')
        pyplot.plot(self.time_vector, Z, label='Zombies')
        pyplot.xlabel('Days from outbreak')
        pyplot.ylabel('Population')
        pyplot.title(self.plot_title)
        pyplot.legend(loc=0)
        pyplot.savefig(file_object, format='png')
