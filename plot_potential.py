import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
plot_potential.py

Draw individual potentials that make up force fields.
Output graphs are modeled to match those of ref:
https://cmm.cit.nih.gov/intro_simulation/node15.html

Feel free to reuse these plots or code as long as you cite!

Author:  Victoria T. Lim
Version: 4 May 2021

"""

class Potential:
    def __init__(self, filename, x_range=None, style_xkcd=False):

        if style_xkcd:
            plt.xkcd()

        # create figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # don't plot edges
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # no ticks
        plt.xticks([])
        plt.yticks([])

        self._fig = fig
        self._ax = ax
        self._filename = filename
        self._x_range = x_range

    @property
    def fig(self):
        """Getter for fig."""
        return self._fig

    @property
    def ax(self):
        """Getter for ax."""
        return self._ax

    @property
    def filename(self):
        """Getter for filename."""
        return self._filename

    @property
    def x_range(self):
        """Getter for x_range."""
        return self._x_range


    def finalize_mpl_figure(self):
        ax = self.ax
        filename = self.filename

        [i.set_linewidth(8.) for i in ax.spines.values()]
        plt.savefig(filename, bbox_inches='tight', transparent=True)


    def bond(self, x_range=[-4, 4.2, 0.2], k=10):
        ax = self.ax

        # set xrange and define function
        x = np.arange(x_range[0], x_range[1], x_range[2])
        y = 0.5*k*(x**2)

        # set plot boundaries
        ax.set_xlim([-50, 200])
        ax.set_ylim([-2, 100])

        # plot
        plt.plot(y, color='b', lw=8.)
        self.finalize_mpl_figure()


    def angle(self, x_range=[-8, 8.2, 0.2], k=5):
        ax = self.ax

        # set xrange and define function
        x = np.arange(x_range[0], x_range[1], x_range[2])
        y = 0.5*k*(x**2)

        # set plot boundaries
        ax.set_xlim([-50, 200])
        ax.set_ylim([-2, 200])

        # plot
        plt.plot(y, color='b', lw=8.)
        self.finalize_mpl_figure()


    def torsion(self, x_range=[0, 4.*np.pi, 1000]):
        ax = self.ax

        # set xrange and define function
        x = np.linspace(x_range[0], x_range[1], x_range[2])
        y = np.cos(x)+1

        # set plot boundaries
        ax.set_xlim([0, 15])
        ax.set_ylim([0, 2.5])

        # plot
        plt.plot(x, y, color='b', lw=8.)
        self.finalize_mpl_figure()


    def improper(self, x_range=[-8, 8.2, 0.2]):
        ax = self.ax

        # set xrange and define function
        x = np.arange(x_range[0], x_range[1], x_range[2])
        y = 0.5*5*(x)**2

        # set plot boundaries
        ax.set_xlim([40, 200])
        ax.set_ylim([-2, 200])

        # plot
        ax.set_clip_box(None)
        plt.plot(y, color='b', lw=8., clip_on=False)
        self.finalize_mpl_figure()


    def vdw(self, x_range=[0.1, 10, 0.1], eps=1.77, sig=4.10):
        ax = self.ax
        ax.spines['bottom'].set_color('none')

        # set xrange and define function
        x = np.arange(x_range[0], x_range[1], x_range[2])
        y = 4*eps*((sig/x)**12.-(sig/x)**6.)

        # set plot boundaries
        ax.set_xlim([3, 12])
        ax.set_ylim([-2, 2])

        # plot
        plt.axhline(y=0.3, c='k', lw=8.)
        plt.plot(x, y, color='b', lw=8.)
        self.finalize_mpl_figure()


    def electrostatic(self, x_range=[0.2, 8.3, 0.2]):
        ax = self.ax
        ax.spines['bottom'].set_color('none')

        # set xrange and define function
        x = np.arange(x_range[0], x_range[1], x_range[2])
        y = -2/x

        # set plot boundaries
        ax.set_ylim([-10, 2])

        # plot
        plt.axhline(y=0.5, c='k',lw=8.)
        plt.plot(x, y, color='b', lw=8.)
        self.finalize_mpl_figure()


    def morse(self, x_range=[-3, 12, 0.1], const_de=1., const_a=0.5, const_re=0.):
        ax = self.ax
        ax.spines['left'].set_color('none')
        ax.spines['bottom'].set_color('none')

        # set xrange and define function
        # https://en.wikipedia.org/wiki/Morse_potential
        r = np.arange(x_range[0], x_range[1], x_range[2])
        y = const_de * ( np.exp(-2*const_a*(r-const_re)) - 2*np.exp(-1*const_a*(r-const_re)) )

        # set plot boundaries
        ax.set_xlim([-5, 14])
        ax.set_ylim([-2, 2])

        # plot
        plt.plot(r, y, color='b', lw=8.)
        self.finalize_mpl_figure()


def draw_spiral(filename, nloops, axis, centerline=False):
    """
    Draw a spiral to represent a spring.

    Parameters
    ----------
    filename : string
        name of output image filename
    nloops : float
        number of loops in the spring
    axis : string
        'x' 'y' 'z' representing direction of spring
    centerline : Bool
        whether or not a central axis should be drawn through spring

    Reference
    ---------
    Code modified from https://scipython.com/book/chapter-7-matplotlib/examples/depicting-a-helix/

    """

    n = 1000
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot a helix along the specified axis
    theta_max = nloops*2 * np.pi

    # futz with first number to change where spiral starts (e.g., 0)
    theta = np.linspace(-np.pi/3, theta_max, n)

    if axis.lower()=='x':
        x = theta
        y = np.cos(theta)
        z = np.sin(theta)
    elif axis.lower()=='y':
        y = theta
        z = np.cos(theta)
        x = np.sin(theta)
    elif axis.lower()=='z':
        z = theta
        x = np.cos(theta)
        y = np.sin(theta)

    # plot the spiral
    ax.plot(x, y, z, 'b', lw=8)

    # line through the centre of the helix
    if centerline:
        if axis.lower()=='x':
            xx = (-theta_max*0.2, theta_max * 1.2)
            yy = (0, 0)
            zz = (0, 0)
        if axis.lower()=='y':
            xx = (0, 0)
            yy = (-theta_max*0.2, theta_max * 1.2)
            zz = (0, 0)
        if axis.lower()=='z':
            xx = (0, 0)
            yy = (0, 0)
            zz = (-theta_max*0.2, theta_max * 1.2)

        ax.plot(xx, yy, zz, color='k', lw=2)

    # remove axis planes, ticks and labels
    ax.set_axis_off()
    plt.savefig(filename, bbox_inches='tight', transparent=True)


Potential("potential_bond.png").bond()
Potential("potential_angle.png").angle()
Potential("potential_torsion.png").torsion()
Potential("potential_improper.png").improper()
Potential("potential_vdw.png").vdw()
Potential("potential_electrostatic.png").electrostatic()
Potential("potential_morse.png").morse()

draw_spiral('spring_x.png', 3.3333, 'x')
draw_spiral('spring_x_centerline.png', 3.3333, 'x', True)
draw_spiral('spring_y.png', 3.3333, 'y')
draw_spiral('spring_y_centerline.png', 3.3333, 'y', True)
draw_spiral('spring_z.png', 3.3333, 'z')
draw_spiral('spring_z_centerline.png', 3.3333, 'z', True)

