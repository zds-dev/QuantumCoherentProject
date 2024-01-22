from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np
import matplotlib.pyplot as plt

def create_W_state(bool=0):
    q = QuantumRegister(3)
    b = ClassicalRegister(3)
    circuit = QuantumCircuit(q, b)
    circuit.ry(2*np.arcos(1/np.sqrt(3)),q[0])
    circuit.ch(q[0],q[1])
    circuit.ccx(q[0],q[1],q[2])
    circuit.x(q[0])
    circuit.x(q[1])
    circuit.cx(q[0],q[1])
    return(circuit,q,b)

def measure_arbitrary(circuit, q, b, bit=0, theta=0, phi=0, delay=0):

    circuit.rz(-phi, q[bit])
    circuit.ry(-theta, q[bit])
    circuit.measure(bit, bit)
    return circuit, q, b
    
        