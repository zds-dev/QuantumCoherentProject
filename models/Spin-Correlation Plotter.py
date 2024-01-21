import numpy as np
import matplotlib.pyplot as plt

def qubit_creator(coefficient_a):
    b = np.sqrt(1 - coefficient_a**2)
    qubit = np.array([coefficient_a,b])
    return(qubit)

def two_qubit_product_state_creator(qubit1,qubit2):
    state = np.kron(qubit1,qubit2)
    return(state)

def three_qubit_product_state_creator(qubit1,qubit2,qubit3):
    int_state = np.kron(qubit1,qubit2)
    state = np.kron(qubit3,int_state)
    return(state)

def general_two_state_creator(product_state1,product_state2,coefficient_1):
    b = np.sqrt(1 - coefficient_1**2)
    state = coefficient_1*product_state1 + b*product_state2
    return(state)
    
def general_three_state_creator(product_state1,product_state2,product_state3,coefficient_1,coefficient_2):
    c = np.sqrt(1 - ((coefficient_1**2)+(coefficient_2**2)))
    state = coefficient_1*product_state1 + coefficient_2*product_state2 + c*product_state3
    return(state)
    

def spin_measurement_op(theta,phi):
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)
    return(np.array([[z,x-(1j*y)],[x+(1j*y),-z]]))

def two_qubit_spin_corr_expectation(state,direction_1_theta,direction_1_phi,
                                  direction_2_theta,direction_2_phi):  
    state_hor = np.reshape(state,(1,4))
    state_ver = np.reshape(state,(4,1))
    op = np.kron(spin_measurement_op(direction_1_theta,direction_1_phi),
            spin_measurement_op(direction_2_theta,direction_2_phi))
    return(np.matmul(state_hor,(np.matmul(op,state_ver))))


def three_qubit_spin_corr_expectation(state,direction_1_theta,direction_1_phi,
                                  direction_2_theta,direction_2_phi,
                                  direction_3_theta,direction_3_phi):  
    state_hor = np.reshape(state,(1,8))
    state_ver = np.reshape(state,(8,1))
    inter = np.kron(spin_measurement_op(direction_1_theta,direction_1_phi),
                    spin_measurement_op(direction_2_theta,direction_2_phi))
    op = (np.kron(inter,spin_measurement_op(direction_1_theta,direction_1_phi)))
    
    return(np.matmul(state_hor,(np.matmul(op,state_ver))))
    
resolution = 100
theta_value_range = np.linspace(0,np.pi,resolution)
phi_value_range = np.linspace(0,2*np.pi,resolution)

# W-state
a = qubit_creator(0)
b = qubit_creator(1)
prod1 = three_qubit_product_state_creator(a,a,b)
prod2 = three_qubit_product_state_creator(a,b,a)
prod3 = three_qubit_product_state_creator(b,a,a)
state = general_three_state_creator(prod1, prod2, prod3, 1/np.sqrt(3), 1/np.sqrt(3))
x_values = np.zeros([resolution,resolution])
y_values = np.zeros([resolution,resolution])
z_values = np.zeros([resolution,resolution])
theta_values = np.zeros([resolution,resolution])
phi_values = np.zeros([resolution,resolution])
correlation_values = np.zeros([resolution,resolution])
i=0
n=0

for phi in phi_value_range:
    for theta in theta_value_range:
        val = np.real(three_qubit_spin_corr_expectation(state,theta,phi,theta,phi,theta,phi))
        x_values[i,n]=val*np.sin(theta)*np.cos(phi)
        y_values[i,n]=val*np.sin(theta)*np.sin(phi)
        z_values[i,n] =val*np.cos(theta)
        theta_values[i,n]=theta
        phi_values[i,n]=phi
        correlation_values[i,n] = val
        i+=1
    i=0
    n+=1
    
fig = plt.figure(1)
ax=fig.gca(projection='3d')
surf = ax.plot_surface(x_values,y_values,z_values)   

fig = plt.figure(2)
ax=fig.gca(projection='3d')
surf = ax.plot_surface(theta_values,phi_values,correlation_values) 

fig = plt.figure(3) # Takes x-z plane
ax=fig.gca()
surf = ax.plot(theta_values,correlation_values[:,0])
