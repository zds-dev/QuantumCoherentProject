# Connect to Quantum Inspire QI using TOKEN file.
import models.connect_quantum_inspire as qi_tools
import models.quantum_state_circuits as qs_circuits
import importlib
import numpy as np
import matplotlib.pyplot as plt

importlib.reload(qi_tools)
importlib.reload(qs_circuits)

QI = qi_tools.connect_qi('../TOKEN')
qi_backend = QI.get_backend('QX single-node simulator')

theta_vals = np.linspace(0, np.pi, 6)
phi_vals = np.zeros_like(theta_vals)
measurement_directions = np.array([theta_vals, phi_vals, theta_vals, phi_vals])

circuit, q,b = qs_circuits.create_entangled_singlet()
circuit.barrier()
expectation_list_singlet = qs_circuits.measure_circuit_directions(circuit, q, b, measurement_directions, qi_backend, shots=512)