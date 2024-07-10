import numpy as np
import matplotlib.pyplot as plt

# motor param
class MotorParams:
    def __init__(self, resistance, inductance, KV, voltage, no_load_current):
        self.resistance = resistance
        self.inductance = inductance
        self.KV = KV
        self.voltage = voltage
        self.no_load_current = no_load_current
        self.torque_const = 60 / (2 * 3.14159265 * KV)
        self.stall_current = voltage / resistance
        print("torque const: ", self.torque_const)
        print("stall current: ", self.stall_current)
        self.current_array = np.linspace(0, self.stall_current, 1000)
        self.stall_torque = self.torque_const * (self.stall_current - self.no_load_current)
        self.torque_array = self.torque_const * (self.current_array - self.no_load_current)
        self.torque_array = np.maximum(self.torque_array, 0)
        self.omega_array = (voltage - resistance * (self.current_array + self.no_load_current)) / self.torque_const
        self.omega_array = np.maximum(self.omega_array, 0)
        self.power_array = self.omega_array * self.torque_array
        self.power_array_2 = voltage * (self.current_array - self.no_load_current) - resistance * self.current_array ** 2
        self.efficiency_array = self.power_array / (voltage * self.current_array)

motors = []
motors.append(MotorParams(68e-3, 0.5e-3, 65, 24, 0.7))
motors.append(MotorParams(68e-3 * 2, 0.5e-3 * 2, 65 / 2, 24, 0.7))
motors.append(MotorParams(68e-3 / 2, 0.5e-3 / 2, 65, 24, 0.7 * 2))
motors.append(MotorParams(68e-3, 0.5e-3, 65 * 2, 24, 0.7))

plot_num = 3

plt.subplot(1, plot_num, 1)
for motor in motors:
    plt.plot(motor.torque_array, motor.omega_array)
plt.xlabel("Torque (Nm)")
plt.ylabel("Speed (rad/s)")

plt.subplot(1, plot_num, 2)
for motor in motors:
    plt.plot(motor.torque_array, motor.power_array)
    # plt.plot(motor.torque_array, motor.power_array_2)
plt.xlabel("Torque (Nm)")
plt.ylabel("Power (W)")

plt.subplot(1, plot_num, 3)
for motor in motors:
    plt.plot(motor.torque_array, motor.efficiency_array)
plt.xlabel("Torque (Nm)")
plt.ylabel("Efficiency")

plt.show()


