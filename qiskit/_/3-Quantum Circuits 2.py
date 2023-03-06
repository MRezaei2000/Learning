#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit import QuantumCircuit, Aer, assemble
from qiskit import *
import numpy as np
from math import sqrt, pi
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit import QuantumCircuit, assemble, Aer
from qiskit.visualization import plot_histogram, plot_bloch_vector
from qiskit.quantum_info import Statevector


# In[2]:


from qiskit_textbook.widgets import binary_widget
binary_widget(nbits=5)


# In[3]:


qc_output = QuantumCircuit(6)
qc_output.measure_all()
qc_output.draw('mpl',initial_state=True)


# In[4]:


backend = Aer.get_backend('aer_simulator').run(qc_output).result().get_counts()
plot_histogram(backend)


# In[5]:


qc_encode = QuantumCircuit(8)
qc_encode.x(7)
qc_encode.draw()


# In[6]:


qc_encode.measure_all()
qc_encode.draw()


# In[7]:


sim = Aer.get_backend('aer_simulator') 
result = sim.run(qc_encode).result()
counts = result.get_counts()
plot_histogram(counts)


# In[8]:


qc_cnot = QuantumCircuit(2)
qc_cnot.cx(0,1)
qc_cnot.draw()


# In[9]:


qc = QuantumCircuit(2,2)
qc.x(0)
qc.cx(0,1)
qc.measure(0,0)
qc.measure(1,1)
qc.draw()


# In[10]:


qc_ha = QuantumCircuit(4,2)
# encode inputs in qubits 0 and 1
qc_ha.x(0) # For a=0, remove this line. For a=1, leave it.
qc_ha.x(1) # For b=0, remove this line. For b=1, leave it.
qc_ha.barrier()
# use cnots to write the XOR of the inputs on qubit 2
qc_ha.cx(0,2)
qc_ha.cx(1,2)
qc_ha.barrier()
# extract outputs
qc_ha.measure(2,0) # extract XOR value
qc_ha.measure(3,1)

qc_ha.draw()


# In[11]:


qc_ha = QuantumCircuit(4,2)
# encode inputs in qubits 0 and 1
qc_ha.x(0) # For a=0, remove the this line. For a=1, leave it.
qc_ha.x(1) # For b=0, remove the this line. For b=1, leave it.
qc_ha.barrier()
# use cnots to write the XOR of the inputs on qubit 2
qc_ha.cx(0,2)
qc_ha.cx(1,2)
# use ccx to write the AND of the inputs on qubit 3
qc_ha.ccx(0,1,3)
qc_ha.barrier()
# extract outputs
qc_ha.measure(2,0) # extract XOR value
qc_ha.measure(3,1) # extract AND value

qc_ha.draw()


# In[12]:


qobj = assemble(qc_ha)

result = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
plot_histogram(result)


# In[13]:



qc = QuantumCircuit(1)  # Create a quantum circuit with one qubit
initial_state = [0,1]  # Define initial_state as |1>
qc.initialize(initial_state,0)   # Apply initialisation operation to the 0th qubit
qc.draw('mpl')   # Let's view our circuit


# In[14]:


qc = QuantumCircuit(1)  # Create a quantum circuit with one qubit
initial_state = [0,1]   # Define initial_state as |1>
statevector = qc.initialize(initial_state, 0) # Apply initialisation operation to the 0th qubit
qc.save_statevector() # Tell simulator to save statevector
qc.draw('mpl')


# In[15]:


qobj = assemble(qc)     # Create a Qobj from the circuit for the simulator to run
result = Aer.get_backend('aer_simulator').run(qobj).result()
out_state = result.get_statevector()  #result with dictinary statevector interpret
out_state.draw('latex') # Display the output state vector
# or we use eq below
# result = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
# print(result)


# In[16]:


qc.measure_all()
qc.draw('mpl')


# In[17]:


qobj = assemble(qc)
result = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
plot_histogram(result)


# In[18]:


# instead put our qubit into a superposition and see what happens (|q0⟩ = (1/√2)|0⟩ + (i/√2)|1⟩ )
initial_state = [1/sqrt(2), 1j/sqrt(2)]  # Define state |q_0>
qc = QuantumCircuit(1) # Must redefine qc
qc.initialize(initial_state, 0) # Initialize the 0th qubit in the state `initial_state`
qc.save_statevector() # Save statevector
qc.draw('mpl')


# In[19]:


qobj = assemble(qc)
state = Aer.get_backend('aer_simulator').run(qobj).result().get_statevector() # Execute the circuit
state.draw('latex')   # Print the result


# In[20]:


qobj = assemble(qc)
results = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
plot_histogram(results)


# In[21]:


qc.measure_all()
qc.draw('mpl')


# In[22]:


qobj = assemble(qc)
result = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
print (result)


# In[23]:


qc = QuantumCircuit (3,3)
state_0 = Statevector.from_label('1')
state_zero = qc.initialize(state_0 , 0)
state_1 = Statevector.from_label('0')
state_one = qc.initialize(state_1 , 1)
state_2 = Statevector.from_label('1')
state_two = qc.initialize(state_2 , 2 )
qc.barrier()
qc.measure([0,1,2],[0,1,2])
qc.draw('mpl')


# In[24]:


qobj = assemble (qc)
result = Aer.get_backend('aer_simulator').run(qobj).result().get_counts()
plot_histogram(result)


# In[25]:


# Run the code in this cell to interact with the widget
from qiskit_textbook.widgets import state_vector_exercise
state_vector_exercise(target=1/3)


# In[26]:


qc = QuantumCircuit(1) # We are redefining qc
initial_state = [0.+1.j/sqrt(2),1/sqrt(2)+0.j]
qc.initialize(initial_state, 0)
qc.measure_all()
qc.save_statevector()
qc.draw('mpl')


# In[27]:


qobj = assemble(qc)
state = sim.run(qobj).result().get_statevector()
print("State of Measured Qubit =" + str(state))
state.draw('latex')


# In[28]:


coords = [1,pi/2,0]  # [Bloch vector size(Radius) , Theta, Phi]
plot_bloch_vector(coords , coord_type='spherical')


# In[29]:


coords = [1,pi,0]   # plot_bloch_vector for |1⟩
plot_bloch_vector(coords,coord_type ='spherical')


# In[30]:


# plot_bloch_vector for |0⟩
coords = [1,4*pi,0]
plot_bloch_vector(coords,coord_type ='spherical')


# In[31]:


# plot_bloch_vector for 1√2(|0⟩+|1⟩)
coords = [1,pi/4,0]
plot_bloch_vector(coords,coord_type ='spherical')


# In[32]:


# plot_bloch_vector for 1√2(|0⟩-i|1⟩)
coords = [1,pi/4,(3*pi)/2]
plot_bloch_vector(coords,coord_type ='spherical')


# In[33]:


# plot_bloch_vector for 1√2[i,1]
coords = [1,pi/4,(3*pi)/2]  # becuase -i == 1/i 
plot_bloch_vector(coords,coord_type ='spherical')


# In[34]:


# Let's do an X-gate on a |0> qubit
qc = QuantumCircuit(1)
qc.x(0)
qc.draw()


# In[35]:


# Let's see the result
qc.save_statevector()
qobj = assemble(qc)
result = Aer.get_backend('aer_simulator').run(qobj).result().get_statevector()
result.draw('latex')
plot_bloch_multivector(result)


# In[36]:


# Run the code in this cell to see the widget
from qiskit_textbook.widgets import gate_demo
gate_demo(gates='pauli')


# In[37]:


qc = QuantumCircuit(1)
qc.x(0)
qc.save_statevector()
qc.y(0) # Do Y-gate on qubit 0
qc.z(0) # Do Z-gate on qubit 0
qc.draw()


# In[38]:


qc = QuantumCircuit(3)

# Apply H-gate to each qubit:
for qubit in range(3):
    qc.h(qubit)
    
# See the circuit:
qc.draw()


# In[39]:


# Let's see the result
svsim = Aer.get_backend('aer_simulator')
qc.save_statevector()
qobj = assemble(qc)
final_state = svsim.run(qobj).result().get_statevector()

from qiskit.visualization import array_to_latex
array_to_latex(final_state, prefix="\\text{Statevector} = ")


# In[40]:


qc = QuantumCircuit(2)
qc.h(0)
qc.x(1)
qc.draw()

usim = Aer.get_backend('aer_simulator')
qc.save_unitary()
qobj = assemble(qc)
unitary = usim.run(qobj).result().get_unitary()

from qiskit.visualization import array_to_latex
array_to_latex(unitary, prefix="\\text{Circuit = }\n")


# In[41]:


qc = QuantumCircuit(2)
qc.x(1)
qc.draw()

# Simulate the unitary
usim = Aer.get_backend('aer_simulator')
qc.save_unitary()
qobj = assemble(qc)
unitary = usim.run(qobj).result().get_unitary()

array_to_latex(unitary, prefix="\\text{Circuit = } ")


# In[43]:


qc_charlin = QuantumCircuit (2,2)
qc_charlin.ry(1.911,1)
qc_charlin.cx(1,0)
qc_charlin.ry(0.785,0)
qc_charlin.cx(1,0)
qc_charlin.ry(2.356,0)
qc_charlin.draw('mpl')


# In[44]:


meas_zz = QuantumCircuit (2,2)
meas_zz.measure([0,1],[0,1])
meas_zz.draw('mpl')


# In[45]:


from qiskit.visualization import plot_histogram
result = Aer.get_backend('aer_simulator').run(qc_charlin.compose(meas_zz)).result().get_counts()
plot_histogram = plot_histogram (result)
display ( 'Results for z measurements:',result , plot_histogram )


# In[46]:


meas_zx = QuantumCircuit (2,2)
meas_zx.h(0)
meas_zx.measure([0,1],[0,1])

from qiskit.visualization import plot_histogram
result = Aer.get_backend('aer_simulator').run(qc_charlin.compose(meas_zx)).result().get_counts()
plot_histogram = plot_histogram (result)
display ('Results for a z and an x measurement:',result , plot_histogram )


# In[47]:


meas_xz = QuantumCircuit (2,2)
meas_xz.h(1)
meas_xz.measure([0,1],[0,1])

from qiskit.visualization import plot_histogram
result = Aer.get_backend('aer_simulator').run(qc_charlin.compose(meas_xz)).result().get_counts()
plot_histogram = plot_histogram (result)
display ('Results for a x and an z measurement:',result , plot_histogram )


# In[48]:


meas_xx = QuantumCircuit (2,2)
meas_xx.h([0,1])
meas_xx.measure([0,1],[0,1])

from qiskit.visualization import plot_histogram
result = Aer.get_backend('aer_simulator').run(qc_charlin.compose(meas_xx)).result().get_counts()
plot_histogram = plot_histogram (result)
display ('Results for an x and an x measurement:',result , plot_histogram )

