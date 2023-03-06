#!/usr/bin/env python
# coding: utf-8

# In[26]:


#purpose ofquantum teleportation is to transmit an unknown quantum state ofa qubit using two classical bits


# In[5]:


import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
from qiskit.result import marginal_counts
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor


# In[6]:


# setup
qr = QuantumRegister(3, name="q")  
# q0 = State that we want to teleport
# q1 = Alice's half of the Bell pair
# q2 = Bob's half of the Bell pair, the destination of the teleportation

crz = ClassicalRegister(1, name="crz") 
crx = ClassicalRegister(1, name="crx") 
teleportation_circuit = QuantumCircuit(qr, crz, crx)


# In[7]:


# Step 1:create an entangled Bell pair
def create_bell_pair(qc, a, b): 
    qc.h(a) 
    qc.cx(a,b) 
    
create_bell_pair(teleportation_circuit, 1, 2)


# In[8]:


#Step2:Alice applies CNOT followed by H to this state
def alice_gates(qc, psi, a):
    qc.barrier()
    qc.cx(psi, a)
    qc.h(psi)

alice_gates(teleportation_circuit, 0, 1)


# In[9]:


#Step 3:Alice measures both qubits 0 and 1
def measure_and_send(qc, a, b):
    qc.barrier()
    qc.measure(a,0)
    qc.measure(b,1)

measure_and_send(teleportation_circuit, 0 ,1)


# In[10]:


#step 4:Bob applies gates depending For when our message is |11>
def bob_gates(qc, qubit, crz, crx):
    qc.x(qubit).c_if(crx, 1)  
    qc.z(qubit).c_if(crz, 1) 

bob_gates(teleportation_circuit, 2, crz, crx)


# In[11]:


#Porthole testing on a quantum computer
psi = random_statevector(2)
display(array_to_latex(psi, prefix="|\\psi\\rangle ="))


# In[12]:


init_gate = Initialize(psi)
init_gate.label = "init"


# In[13]:


## SETUP
qr = QuantumRegister(3, name="q")   
crz = ClassicalRegister(1, name="crz") 
crx = ClassicalRegister(1, name="crx")
qc = QuantumCircuit(qr, crz, crx)

## STEP 0
qc.append(init_gate, [0])
qc.barrier()

## STEP 1
create_bell_pair(qc, 1, 2)
qc.barrier()

## STEP 2
alice_gates(qc, 0, 1)

## STEP 3
measure_and_send(qc, 0, 1)

## STEP 4
bob_gates(qc, 2, crz, crx)

qc.draw('mpl')


# In[14]:


#simulator
sim = Aer.get_backend('aer_simulator')
qc.save_statevector()
out_vector = sim.run(qc).result().get_statevector()
plot_bloch_multivector(out_vector)


# In[15]:


#Since all quantum gates are reversible, we can find the inverse of these gates using
inverse_init_gate = init_gate.gates_to_uncompute()


# In[16]:


## SETUP
qr = QuantumRegister(3, name="q")   
crz = ClassicalRegister(1, name="crz") 
crx = ClassicalRegister(1, name="crx")
qc = QuantumCircuit(qr, crz, crx)

## STEP 0
qc.append(init_gate, [0])
qc.barrier()

## STEP 1 
create_bell_pair(qc, 1, 2)
qc.barrier()

## STEP 2
# Send q1 to Alice and q2 to Bob
alice_gates(qc, 0, 1)

## STEP 3
measure_and_send(qc, 0, 1)

## STEP 4
bob_gates(qc, 2, crz, crx)

## STEP 5
# reverse the initialization process
qc.append(inverse_init_gate, [2])

qc.draw('mpl')   #inverse_init_gate appearing, labelled 'disentangler' on the circuit


# In[17]:


# Need to add a new ClassicalRegister
cr_result = ClassicalRegister(1)
qc.add_register(cr_result)
qc.measure(2,2)
qc.draw('mpl')


# In[18]:


#we have a 100% chance of measuring q2 in the state |0⟩
t_qc = transpile(qc, sim)
t_qc.save_statevector()
counts = sim.run(t_qc).result().get_counts()
qubit_counts = [marginal_counts(counts, [qubit]) for qubit in range(3)]
plot_histogram(counts )


# In[19]:


#Teleportation on a Real Quantum Computer
def new_bob_gates(qc, a, b, c):
    qc.cx(b, c)
    qc.cz(a, c)


# In[20]:


qc = QuantumCircuit(3,1)
 
qc.append(init_gate, [0])
qc.barrier()

create_bell_pair(qc, 1, 2)
qc.barrier()

alice_gates(qc, 0, 1)
qc.barrier()

new_bob_gates(qc, 0, 1, 2)

qc.append(inverse_init_gate, [2])

qc.measure(2,0)

qc.draw('mpl')


# In[ ]:


IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')


# In[ ]:


backend = least_busy(provider.backends(filters=lambda b: b.configuration().n_qubits >= 3 and
                                   not b.configuration().simulator and b.status().operational==True))
t_qc = transpile(qc, backend, optimization_level=3)
job = backend.run(t_qc)
job_monitor(job)


# In[ ]:


# Get the results and display them
exp_result = job.result()
exp_counts = exp_result.get_counts(qc)
print(exp_counts)
plot_histogram(exp_counts)


# In[ ]:


print(f"The experimental error rate : {exp_counts['1']*100/sum(exp_counts.values()):.3f}%")

