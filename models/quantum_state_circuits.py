from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute
import numpy as np

def create_product_state(bool=0, off=False):
    # |00> or |11>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    if bool:
        circuit.x(q[0])
        if not off:
            circuit.x(q[1])
    else:
        if off:
            circuit.x(q[1])

    return circuit, q, b


def create_mix_state():
    # |00> + |01> + |10> + |11>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.h(q[0])
    circuit.h(q[1])
    return circuit, q, b

def create_unentangled_sum():
    #|00> + |01>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.h(q[0])
    return circuit, q, b

def create_unentangle_diff():
    #|00> - |01>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.x(q[0])
    circuit.h(q[0])
    return circuit, q, b

def create_entangled_triplet():
    # |01> + |10>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.x(q[0])
    circuit.h(q[1])
    circuit.cx(q[1], q[0])
    return circuit, q, b


def create_entangled_singlet():
    # |01> - |10>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.initialize('00')
    circuit.x(q[0])
    circuit.x(q[1])
    circuit.h(q[1])
    circuit.cx(q[1], q[0])
    return circuit, q, b


def measure_x(circuit, q, b, bit=0):
    circuit.h(q[bit])
    circuit.measure(q[bit], b[bit])
    return circuit, q, b

def measure_y(circuit, q, b, bit=0):
    circuit.sdg(q[bit])
    circuit.h(q[bit])
    circuit.measure(q[bit], b[bit])
    return circuit, q, b

def measure_z(circuit, q, b, bit=0):
    circuit.measure(bit, bit)
    return circuit, q, b

def measure_arbitrary(circuit, q, b, bit=0, theta=0, phi=0, delay=0):
    # Measure at an arbitrary angle therefore rotate axis by negative angle
    # To test properly should be equivalent to measure_x when theta=pi/2 and phi=0
    circuit.rz(-phi, q[bit])
    circuit.ry(-theta, q[bit])
    circuit.measure(bit, bit)
    return circuit, q, b


def measure_circuit_directions(circuit, q, b, measurement_directions, backend, shots=1000):
    expectation_list = []
    results = {'00': [], '01': [], '10': [], '11': []}
    jobs = []
    for i in range(np.size(measurement_directions, 1)):
        icircuit = circuit.copy()
        theta1 = measurement_directions[0, i]
        phi1 = measurement_directions[1, i]
        theta2 = measurement_directions[2, i]
        phi2 = measurement_directions[3, i]

        icircuit, q, b = measure_arbitrary(icircuit, q, b, 0, theta1, phi1)
        icircuit, q, b = measure_arbitrary(icircuit, q, b, 1, theta2, phi2)
        jobs.append(icircuit.copy())

    qi_job = execute(jobs, initial_layout={q[0]:1, q[1]:2}, backend=backend, shots=shots)
    qi_result = qi_job.result()

    for i,job in enumerate(jobs):
        probabilities_histogram = qi_result.get_probabilities(i)
        spins = [-(sum(map(int, list(state))) % 2 * 2 - 1) for state, val in probabilities_histogram.items()]
        expectation_list.append(sum([spins[i] * val for i, val in enumerate(probabilities_histogram.values())]))
        # variance_list.append(np.var([spins[i]*val for i, val in enumerate(probabilities_histogram.values())]))
        for key in results.keys():
            if key not in probabilities_histogram.keys():
                results[key].append(0)
            else:
                results[key].append(probabilities_histogram[key])

    return expectation_list, results

def measure_circuit_delays(circuit, q, b, delays, theta1, phi1, theta2, phi2, backend, shots=1000):
    expectation_list = []
    results = {'00': [], '01': [], '10': [], '11': []}

    items = np.size(delays)
    # If delays is longer then 20, split into multiple jobs, otherwise QI will reject
    jobs_lim = 20
    for j in range(items//jobs_lim+1):
        jobs = []
        for i in range(max(0, j*jobs_lim), min(items, (j+1)*jobs_lim)):
            icircuit = circuit.copy()
            icircuit.barrier()
            icircuit.delay(int(delays[i]))
            icircuit.barrier()
            icircuit, q, b = measure_arbitrary(icircuit, q, b, 0, theta1, phi1)
            icircuit, q, b = measure_arbitrary(icircuit, q, b, 1, theta2, phi2)
            jobs.append(icircuit.copy())

        if len(jobs)>0:
            qi_job = execute(jobs, initial_layout={q[0]:1, q[1]:2}, backend=backend, shots=shots)
            qi_result = qi_job.result()

            for i in range(min(items, (j+1)*jobs_lim)-max(0, j*jobs_lim)):
                probabilities_histogram = qi_result.get_probabilities(i)
                spins = [-(sum(map(int, list(state))) % 2 * 2 - 1) for state, val in probabilities_histogram.items()]
                expectation_list.append(sum([spins[i] * val for i, val in enumerate(probabilities_histogram.values())]))
                # variance_list.append(np.var([spins[i]*val for i, val in enumerate(probabilities_histogram.values())]))
                for key in results.keys():
                    if key not in probabilities_histogram.keys():
                        results[key].append(0)
                    else:
                        results[key].append(probabilities_histogram[key])

    return expectation_list, results