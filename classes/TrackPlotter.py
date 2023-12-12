import matplotlib.pyplot as plt
import pandas as pd

from classes.Vector import Vector
from classes.Optimizer import Optimizer

class TrackPlotter:
    def __init__(self, circuit):
        self.circuit = circuit
        self.track = pd.read_csv('./tracks/' + self.circuit + '.csv')
        self.track.columns = ['x','y','r','l']
        self.make_track()


    def make_track(self):
        right_x, right_y, left_x, left_y,vector = [], [], [], [],[]
        for i in range(self.track.shape[0]):
            if i == self.track.shape[0] - 1:
                v = Vector(self.track['x'][0] - self.track['x'][i], self.track['y'][0] - self.track['y'][i])
            else:
                v = Vector(self.track['x'][i + 1] - self.track['x'][i], self.track['y'][i + 1] - self.track['y'][i])
            vector.append(v.norm())
            r = v.right().norm() * self.track['r'][i]
            l = v.left().norm() * self.track['l'][i]
            right_x.append((self.track['x'][i] + r.x))
            right_y.append((self.track['y'][i] + r.y))
            left_x.append((self.track['x'][i] + l.x))
            left_y.append((self.track['y'][i] + l.y))

        self.right_x = right_x
        self.right_y = right_y
        self.left_x = left_x
        self.left_y = left_y
        self.norm = vector


    def draw_track(self, racingline:bool = False, save:bool = False):
        plt.figure(figsize=(8,8))
        plt.axes().set_aspect('equal')
        xrange = max(max(self.right_x),max(self.left_x)) - min(min(self.right_x), min(self.left_x))
        yrange = max(max(self.right_y), max(self.left_y)) - min(min(self.right_y), min(self.left_y))
        if xrange>yrange:
            plt.xlim([min(min(self.right_x),min(self.left_x)) - xrange//10,  max(max(self.right_x), max(self.left_x)) + xrange//10])
        else:
            plt.ylim([min(min(self.right_y), min(self.left_y)) - yrange//10, max(max(self.right_y), max(self.left_y)) + yrange//10])

        plt.title('Ideal Racing Line in '+ self.circuit + ' Circuit')
        plt.plot(self.right_x, self.right_y, c='red', linewidth = 0.5)
        plt.plot(self.left_x, self.left_y, c='red',linewidth = 0.5)

        if racingline:
            plt.plot(self.ix, self.iy, c='blue',linewidth = 1)

        if save:
            plt.savefig('./' + self.circuit + '.png',format='png')

        plt.show()

    def optimization(self, node_size, max_velocity,min_velocity,velocity_interval, max_theta, theta_interval,save):
        self.optimizer = Optimizer(rx=self.right_x, ry=self.right_y, lx=self.left_x, ly=self.left_y, norm=self.norm,
                                   node_size=node_size, max_velocity=max_velocity,min_velocity=min_velocity,velocity_interval=velocity_interval, max_theta=max_theta, theta_interval= theta_interval)
        self.ix,self.iy = self.optimizer.optimization()
        self.draw_track(racingline = True, save=save)