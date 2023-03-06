#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Start learning Qiskit


# In[ ]:


# Performing operations with Operator and Statevector


# In[18]:


from numpy import array
from numpy import matmul
from qiskit.quantum_info import Statevector
from numpy import sqrt
from qiskit.quantum_info import Operator
from numpy import sqrt , pi , exp


# In[3]:


#Vectors and matrices in Python
ket1=array([1,0])
ket2=array([0,1])
display(ket1/2+ket2/2)


# In[4]:


display (matmul(ket1,ket2))


# In[7]:


# Statevector in Qiskit
ket_1 = Statevector ([0,1])
display (ket_1)


# In[8]:


display (ket_1.draw ('latex'))


# In[9]:


ket_0 = Statevector ([1,0])
display (ket_0.draw('latex'))


# In[11]:


ket_plus = Statevector ([1/sqrt(2), 1/sqrt(2)])
display (ket_plus.draw('latex'))


# In[12]:


ket_example = Statevector ([1/3,2/3])
display (ket_example.draw('latex'))


# In[15]:


# With command is.valid , we can check whether that state is quantum correct or not
display (ket_plus.is_valid())


# In[16]:


display (ket_example.is_valid())
# Why is the answer false? Because ket_example is not normal in terms of quantum mechanics


# In[13]:


#Counting example of |0> in a classic way
statistics_ket0 = ket_0.sample_counts(1000)
display (statistics_ket0)


# In[14]:


#Counting example of |+> in a classic way
statistics_ket_plus = ket_plus.sample_counts(1000)
display(statistics_ket_plus)


# In[23]:


# Unitary operations can be defined and performed on state vectors in Qiskit using the Operator class

X = Operator([ [0,1],[1,0] ])
Y = Operator([ [0,-1.j],[1.j,0] ])
Z = Operator([ [1,0],[0,-1] ])
H = Operator([ [1/sqrt(2),1/sqrt(2)],[1/sqrt(2),-1/sqrt(2)] ])
S = Operator([ [1,0],[0,1.j] ])
T = Operator([ [1,0],[0,(1+1.j)/sqrt(2)] ])


# In[26]:


ket_0 = Statevector([1,0])

gate_x = ket_0.evolve(X)
gate_x.draw('latex')


# In[27]:


gate_Y = ket_0.evolve(Y)
gate_Y.draw('latex')


# In[28]:


gate_z = ket_0.evolve(Z)
gate_z.draw('latex')


# In[29]:


ket_0 = Statevector([1,0])

ket_0 = ket_0.evolve(H)
ket_0 = ket_0.evolve(T)
ket_0 = ket_0.evolve(H)
ket_0 = ket_0.evolve(T)
ket_0 = ket_0.evolve(Z)

ket_0.draw('latex')


# In[31]:


H0= Operator ([[0,0,0,0],[0,0,2,0],[0,2,0,0],[0,0,0,0]])
H1=Operator([[1,0],[0,-1]])
H2=Operator([[1,0],[0,1]])
H3=H1.tensor(H2)

H=(H0+H3)
display(H)


# In[32]:


zero = Statevector.from_label('0') 
zero,one.draw('latex')


# In[22]:


one = Statevector.from_label('1')
one.draw('latex')


# In[23]:


plus = Statevector.from_label('+')
plus.draw('latex')


# In[24]:


minus = Statevector.from_label('-')
minus.draw('latex')


# In[25]:


W = Statevector ([0,1,1,0,1,0,0,0]/sqrt(3))
W.draw('latex')


# In[29]:


result,new_sv = W.measure([0])
print('result = %s\nnew_sv =%s ' %(result,new_sv))


# In[ ]:




