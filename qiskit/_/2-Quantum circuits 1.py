#!/usr/bin/env python
# coding: utf-8

# In[13]:


# circuits : are models of computation in which information is carried by wires through a network of gates


# In[52]:


from qiskit import *
from qiskit.quantum_info import Statevector , Operator
from numpy import sqrt , pi , exp
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.tools.visualization import plot_bloch_multivector


# In[15]:


# simple example of a quantum circuit in Qiskit
# Create quantum circuit with 3 qubits
Circuit = QuantumCircuit (3)
Circuit.draw ()


# In[17]:


# Create quantum circuit with 2 qubits 
circuit = QuantumCircuit (2)
circuit.h(1)
circuit.x(0)
circuit.t(0)
circuit.z(0)
circuit.draw ()


# In[21]:


circuit = QuantumCircuit (1)
circuit.h(0)
circuit.draw('mpl')


# In[22]:


ket0 = Statevector ([1,0])
circuit_ket0 = ket0.evolve(circuit)
circuit_ket0.draw ('latex')


# In[25]:


#let's simulate the result of running this experiment 4000 times
statistics = circuit_ket0.sample_counts(4000)
plot_histogram(statistics)


# In[26]:


qc = QuantumCircuit (1,1)
qc.x(0)
get_ipython().run_line_magic('matplotlib', 'inline')
qc.draw('mpl')


# In[31]:


# Qiskit has a function to plot a Bloch sphere, plot_bloch_vector()
plot_bloch_multivector(ket0)


# In[32]:


one = Statevector.from_label('1')
plot_bloch_multivector(one)


# In[33]:


qc = QuantumCircuit (3)
qc.x(0)
qc.x(1)
qc.ccx(0,1,2)
qc.draw('mpl')


# In[34]:


state_vector = Statevector(qc)
state_vector.draw('latex')


# In[38]:


ket0= Statevector ([1/sqrt(2), 1/sqrt(2)])
ket1= Statevector ([0,1])
ket2= Statevector ([1/3,sqrt(8)/3])
ket3= Statevector ([1,0])

ket = ket0.tensor(ket1)
ket_f = ket.tensor(ket2)
ket__f = ket_f.tensor(ket3)
ket__f.draw('latex')


# In[39]:


qc = QuantumCircuit(4)

qc.x(0)
qc.s(2)
qc.h(1)
qc.t(3)

ket_final = ket__f.evolve(qc)
display(ket_final)


# In[40]:


ket_final.draw('latex')


# In[42]:


plus = Statevector.from_label('+')
i_state = Statevector([1/sqrt(2), 1j/sqrt(2)])
psi = plus.tensor(i_state)

qc_2 = QuantumCircuit (2)
qc_2.i(1)
qc_2.x(0)

result_f = psi.evolve(qc_2)
result_f.draw('latex')


# In[47]:


X = Operator([ [0, 1],[1, 0] ])
I = Operator([ [1, 0],[0, 1] ])
result_final = result_f.evolve(X^I)
result_final.draw('latex')


# In[48]:


CNOT = Operator ([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CNOT_final = result_f.evolve(CNOT)
CNOT_final.draw('latex')


# In[49]:


CNOT = Operator ([[0,0,0,1],[0,0,1,0],[1,0,0,0],[0,1,0,0]])
CNOT_final = result_f.evolve(CNOT)
CNOT_final.draw('latex')


# In[50]:


# Create quantum circuit with 3 qubits and 3 classical bits
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, [1,2])
qc.measure_all()
qc.draw()


# In[53]:


sim = AerSimulator()           # simulator 
job = sim.run(qc)              # run the simulator circuit
result = job.result()          # get the results 
print(result)
result.get_counts()    # interpret the results as a "counts" dictionary


# In[60]:


qc_ = QuantumCircuit (4,2)
qc_.x(0)
qc_.x(1)
qc_.cx(0,2)
qc_.cx(1,2)
qc_.ccx(0,1,3)
qc_.measure(2,0)
qc_.measure(3,1)

qc_.draw()


# In[61]:


sim_ = AerSimulator ()
job_ = sim_5.run (qc_)
result_ = job_5.result ()
result_.get_counts()


# In[59]:


qc_1 = QuantumCircuit (2)
ket = Statevector (qc_1)
qc_1.cx(0,1)
ket.draw('latex')              # why is this happen ? because qubit control is |0>


# In[62]:


qc_2 = QuantumCircuit (2)
qc_2.x(1)
qc_2.cx(1,0)
ket = Statevector(qc_2)
ket.draw('latex')           # why is this happen ? because qubit control is |1>


# In[ ]:




