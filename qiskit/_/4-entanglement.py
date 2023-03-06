#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, Aer, assemble
import numpy as np
from qiskit.visualization import plot_histogram, plot_bloch_multivector


# In[2]:


qc = QuantumCircuit (2)
qc.x(1)
ket = Statevector (qc)
ket.draw('latex')


# In[3]:


qc = QuantumCircuit (2)
ket = Statevector (qc)
qc.x(1)
qc.cx(1,0)
ket_1 = ket.evolve(qc)
ket_1.draw('latex')


# In[4]:


# we are going to created 4 bell state


# In[5]:


qc_1 = QuantumCircuit (2)
qc_1.h(1)
qc_1.cx (1,0)
ket = Statevector (qc_1)
ket.draw('latex')


# In[6]:


qc_2 = QuantumCircuit (2)
qc_2.x(1)
qc_2.h(1)
qc_2.cx(1,0)
ket = Statevector (qc_2)
ket.draw('latex')


# In[7]:


qc_3 = QuantumCircuit (2)
qc_3.x(0)
qc_3.h(1)
qc_3.cx(1,0)
ket = Statevector (qc_3)
ket.draw('latex')


# In[8]:


qc_4 = QuantumCircuit (2)
qc_4.x([0,1])
qc_4.h(1)
qc_4.cx(1,0)
ket = Statevector (qc_4)
ket.draw('latex')


# In[9]:


qc2_ = QuantumCircuit (2)
qc2_.x([0,1])
qc2_.h(0)
qc2_.cx(0,1)
ket = Statevector (qc2_)
ket.draw('latex')


# In[10]:


#  what if control qubit don't have superposition , but target
#  qubit have superposition Again have we entangelment state ?


# In[11]:


qc_9 = QuantumCircuit (2)
qc_9.x([0,1])
qc_9.h(0)
qc_9.cz(0,1)
ket = Statevector (qc_9)
ket.draw('latex')


# In[12]:


qc_9 = QuantumCircuit (2)
qc_9.x([0,1])
qc_9.h(1)
qc_9.cz(0,1)
ket = Statevector (qc_9)
ket.draw('latex')


# In[13]:


qc_a = QuantumCircuit (2)
qc_a.x([1,0])
qc_a.h([1,0])
qc_a.cz(1,0)
ket = Statevector (qc_a)
ket.draw('latex')              # which is entangle


# In[14]:


qc_b = QuantumCircuit (2)
qc_b.cz(0,1)
ket_0 = Statevector.from_label('+')
ket = ket_0.tensor(ket_0)
ket_f = ket.evolve (qc_b)
ket_f.draw('latex')            # which is entangled


# In[15]:


qc_c = QuantumCircuit (2)
qc_c.cz(0,1)
ket_0 = Statevector.from_label('+')
ket_1 = Statevector.from_label('-')
ket_f = ket_0.tensor(ket_1)
ket_final = ket_f.evolve (qc_c)
ket_final.draw('latex')                # which is entangled


# In[16]:


qc_c = QuantumCircuit (2)
qc_c.cz(0,1)
ket_0 = Statevector.from_label('+')
ket_1 = Statevector.from_label('-')
ket_f = ket_1.tensor(ket_0)
ket_final = ket_f.evolve (qc_c)
ket_final.draw('latex')               # which is entangled


# In[17]:


qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0,1)
qc.draw()


# In[ ]:


plot_histogram(result.get_counts())


# In[ ]:


plot_bloch_multivector(final_state)


# In[ ]:


from qiskit.visualization import plot_state_qsphere
plot_state_qsphere(final_state)


# In[ ]:


#Generalised bell_pair
def create_bell_pair():

    qc = QuantumCircuit(2)
    qc.h(1)
    qc.cx(1, 0)
    
    return qc


# In[ ]:




