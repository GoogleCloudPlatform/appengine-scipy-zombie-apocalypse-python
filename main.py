"""A Zombie Apocalypse simulator sample with scipy library."""

import multiprocessing
import os
import StringIO
import urllib

import jinja2
import webapp2

import zombie_apocalypse


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


def simulate(conn, params):
    """Creates a simulation object and generates a resulted png files.

    Then sends the contents of the png file to the parent process.

    Args:
        conn: A pipe object to interact with the parent process.
        params: A dictionary for the simulator constructor.
    """
    simulator = zombie_apocalypse.ZombieApocalypseSimulator(**params)
    image_buffer = StringIO.StringIO()
    simulator.plot(image_buffer)
    conn.send(image_buffer.getvalue())
    conn.close()


def parse_params(request):
    """Parses the WebOb request object and returns a dictionary.

    Args:
        request: a WebOb request object.

    Returns:
        A dict contains values extracted from the request, or the
        default values if not specfied.
    """
    initial_population = float(request.get(
            'initial_population',
            zombie_apocalypse.DEFAULT_INITIAL_POPULATION))
    initial_death_population = float(request.get(
            'initial_death_population',
            zombie_apocalypse.DEFAULT_INITIAL_DEATH_POPULATION))
    birth_rate = float(request.get(
            'birth_rate',
            zombie_apocalypse.DEFAULT_BIRTH_RATE))
    transmission_percent = float(request.get(
            'transmission_percent',
            zombie_apocalypse.DEFAULT_TRANSMISSION_PERCENT))
    return {
        'initial_population': initial_population,
        'initial_death_population': initial_death_population,
        'birth_rate': birth_rate,
        'transmission_percent': transmission_percent,
    }


class MainPage(webapp2.RequestHandler):
    """A handler for showing the simulator form."""

    def get(self):
        """Shows some controllers and an image tag. """
        params = parse_params(self.request)
        template = JINJA_ENVIRONMENT.get_template('index.html')

        image_url = '/draw_simulation?{}'.format(urllib.urlencode(params))
        params['image_url'] = image_url
        self.response.write(template.render(params))


class SimulationImage(webapp2.RequestHandler):
    """A handler for returning a graph showing the simulation result."""

    def get(self):
        """Shows a png graph showing the simulation result.

        We use a child process for generating the png file because the
        matplotlib.pyplot is not threadsafe.
        """
        params = parse_params(self.request)
        parent_conn, child_conn = multiprocessing.Pipe()
        process = multiprocessing.Process(target=simulate,
                                          args=(child_conn, params))
        process.start()
        self.response.headers['content-type'] = 'image/png'
        self.response.write(parent_conn.recv())
        process.join()


APPLICATION = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/draw_simulation.*', SimulationImage),
], debug=True)
