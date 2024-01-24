from quantuminspire.qiskit import QI
QI.set_authentication()
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit import execute
import numpy as np
import matplotlib.pyplot as plt

from quantuminspire.qiskit import QI
qi_backend = QI.get_backend('QX single-node simulator')
QI.set_project_name('W-state Bell')
i=0
resolution = 10
def angle_change_array(shift):
    angle1_change_array = np.array([shift,0,0,shift])
    angle2_change_array = np.array([0,shift,0,shift])
    angle3_change_array = np.array([0,0,shift,shift])
    angle_matrix = np.array([angle1_change_array,angle2_change_array,angle3_change_array])
    return(angle_matrix)
theta_range = np.linspace(0,np.pi/2,10)
bell_array = np.zeros(1)
theta = 0
shift = np.pi/2
change = np.pi/2
rot = 0
bell = []
corr = np.array([0,1,2,3])
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
for itera in angle_change_array(shift)[0,:]:
    theta1_change = angle_change_array(shift)[0,rot]
    theta2_change = angle_change_array(shift)[1,rot]
    theta3_change= angle_change_array(shift)[2,rot]
    phi1_change = angle_change_array(shift)[0,rot]
    phi2_change = angle_change_array(shift)[1,rot]
    phi3_change= angle_change_array(shift)[2,rot]
    circuit1 = circuit.copy()

    circuit1.ry(theta+theta1_change,q[0])
    circuit1.rz(0+phi1_change,q[0])
    
    circuit1.ry(theta+change+theta2_change,q[1])
    circuit1.rz(0+phi2_change,q[1])
    
    circuit1.ry(theta+theta3_change,q[2])
    circuit1.rz(change+phi3_change,q[2])
    
    circuit1.measure(q[0],0)
    circuit1.measure(q[1],1)
    circuit1.measure(q[2],2)
    transpiled_circuit = transpile(circuit1, qi_backend)
    jobs.append(transpiled_circuit.copy())
    rot+=1

qi_job = execute(jobs, qi_backend, shots=4096)
qi_result = qi_job.result().get_counts()

for k in corr:
    counts = qi_result[k]
    if k==3:
        bell.append(-(((counts.get('000',0)+counts.get('110',0)+counts.get('101',0)+counts.get('011',0))-
                    (counts.get('100',0)+counts.get('010',0)+counts.get('001',0)+counts.get('111',0)))/
                   sum(counts.values())))
    else:
        bell.append(((counts.get('000',0)+counts.get('110',0)+counts.get('101',0)+counts.get('011',0))-
                    (counts.get('100',0)+counts.get('010',0)+counts.get('001',0)+counts.get('111',0)))/
                   sum(counts.values()))
bell_array[i]=sum(bell)

print(bell_array)
