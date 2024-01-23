from quantuminspire.qiskit import QI
QI.set_authentication()
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit import execute
import numpy as np
import matplotlib.pyplot as plt

from quantuminspire.qiskit import QI
qi_backend = QI.get_backend('QX single-node simulator')
QI.set_project_name('W-state Spin Correlation 1')

resolution = 10
theta_value_range = np.linspace(0,np.pi,resolution)

i = 0
corr = np.zeros(resolution)
q = QuantumRegister(3)
b = ClassicalRegister(3)
circuit = QuantumCircuit(q, b)
circuit.ry(2*np.arccos(1/np.sqrt(3)),q[0])
circuit.ch(q[0],q[1])
circuit.ccx(q[0],q[1],q[2])
circuit.x(q[0])
circuit.x(q[1])
circuit.cx(q[0],q[1])
jobs = []
for theta in theta_value_range:
    circuit1 = circuit.copy()

    circuit1.ry(-theta,q[0])
    circuit1.ry(-theta,q[1])
    circuit1.ry(-theta,q[2])
    circuit1.measure(q[0],0)
    circuit1.measure(q[1],1)
    circuit1.measure(q[2],2)
    transpiled_circuit = transpile(circuit1, qi_backend)
    jobs.append(transpiled_circuit.copy())

qi_job = execute(jobs, qi_backend, shots=2048)
qi_result = qi_job.result().get_counts()

for k in corr:
    counts = qi_result[i]
    corr[i] = (((counts.get('000',0)+counts.get('110',0)+counts.get('101',0)+counts.get('011',0))-
                (counts.get('100',0)+counts.get('010',0)+counts.get('001',0)+counts.get('111',0)))/
               sum(counts.values()))
    i+=1
        
    
plt.plot(theta_value_range,corr,'*')
