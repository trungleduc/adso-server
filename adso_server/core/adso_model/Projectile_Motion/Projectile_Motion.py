#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from adso_core.component import Component
import numpy
import math


class PointMassSolution:
    """Trajectory of a projectile with air resistance.

    Parameters
    ----------

    mass: float
        Mass of projectile (kg)
    k: float
        Friction coefficient
    speed: float
        Launch speed (m/s)
    angle: float
        Launch angle (deg.)
    x0: ndarray
        Initial position (m)

    Outputs
    -------
        Trajectory, speed and acceleration over time
    """

    def __init__(self, mass: float, k: float, speed: float, angle: float, x0=numpy.zeros(3)):
        g = numpy.r_[0, 0, -9.81]
        angle = math.radians(angle)
        if mass <= 0:
            raise ValueError("Mass must be strictly positive")
        x0 = numpy.asarray(x0)
        v0 = numpy.asarray([speed*math.cos(angle), 0., speed*math.sin(angle)])
        g = numpy.asarray(g)
        self.x0 = x0
        if k > 0:
            omega = k / mass
            tau = 1 / omega
            A = g * tau
        else:
            omega, tau = 0, numpy.inf
            A = numpy.full_like(g, numpy.inf)
        B = v0 - A

        def x_impl(t):
            wt = omega * t
            if wt < 1e-7:  # asymptotic expansion, to avoid exp overflow
                x = x0 + v0 * t + (0.5 * t) * (g * t - wt * v0) * (1 - wt / 3 * (1 - 0.25 * wt))
            else:
                x = x0 + A * t + B * tau * (1 - numpy.exp(-wt))
            return x

        def v_impl(t):
            wt = omega * t
            if wt < 1e-7:  # asymptotic expansion, to avoid exp overflow
                v = v0 + (g * t - v0 * wt) * (1 - wt * (0.5 - wt / 6))
            else:
                v = A + B * numpy.exp(-wt)
            return v
        self.__x = x_impl
        self.__v = v_impl
        self.__a = lambda t: g - self.__v(t) * omega
        self.__omega = omega

    @property
    def omega(self):
        return self.__omega

    def a(self, t):
        return self.__a(t)

    def v(self, t):
        return self.__v(t)

    def x(self, t):
        return self.__x(t)

    def position(self):
        time_step = 0.01
        t = 0.
        position = []
        speed = []
        acceleration = []
        height = self.x0[2]
        while True:
            current_pos = self.x(t)
            spd = self.v(t)
            acc = self.a(t)
            height = current_pos[2]
            if height < 0:
                break
            else:
                position.append([current_pos[0], current_pos[2]])
                speed.append([spd[0], spd[2]])
                acceleration.append([acc[0], acc[2]])
                t += time_step

        return numpy.array(position), numpy.array(speed), numpy.array(acceleration), t


class ProjectileMotion(Component):
    """Demo of Adso component
    """

    def setup(self):
        self.add_input("mass", value=1.5, unit="kg", dtype=float, desc="Mass of projectile", value_range=[0, 10])
        self.add_input("k", value=0.0, dtype=float, desc="Friction coefficient", value_range=[0, 1])
        self.add_input("angle", value=50., unit="degree", dtype=float, desc="Launch angle", value_range=[0, 90])
        self.add_input("speed", value=12.5, unit="m/s", dtype=float, desc="Launch speed", value_range=[0, 20])
        self.add_input("position", value=numpy.array(
            [0, 0, 0.]), dtype=numpy.ndarray, desc="Initial position", value_range=[None, None])

        self.add_output("coordinate", desc="Coordinate of projectile")
        self.add_output("spd", desc="Speed of projectile")
        self.add_output("acc", desc="Acceleration of projectile")
        self.add_output("time", desc="Total time")

    def compute(self):
        solution = PointMassSolution(mass=self.mass, k=self.k, speed=self.speed, angle=self.angle, x0=self.position)
        self.coordinate, self.spd, self.acc, self.time = solution.position()



