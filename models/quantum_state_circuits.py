from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def create_product_state(bool=0):
    # |00> or |11>
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    if bool:
        circuit.x(q[0])
        circuit.x(q[1])
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
