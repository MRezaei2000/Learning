#!/usr/bin/env python
# coding: utf-8

# In[33]:


from qiskit import QuantumCircuit , Aer , IBMQ , transpile, assemble
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor


# In[4]:


# Superdense coding
#Here we will look at one such example,in which transferring one qubit can allow a two bit messageto be sent


# In[5]:


message = '00'
# Alice encodes the message
qc_alice = QuantumCircuit (2,2)
if message [0] == '1':
    qc_alice.x(0)
if message [1] == '1':
    qc_alice.x(1)
# then she creates entangled states
qc_alice.h(1)
qc_alice.cx(1,0)
ket = Statevector (qc_alice)
ket.draw('latex')


# In[6]:


message = '01'
# Alice encodes the message
qc_alice = QuantumCircuit (2,2)
if message [0] == '1':
    qc_alice.x(0)
if message [1] == '1':
    qc_alice.x(1)
# then she creates entangled states
qc_alice.h(1)
qc_alice.cx(1,0)
ket = Statevector (qc_alice)
ket.draw('latex')


# In[7]:


message = '10'
qc_alice = QuantumCircuit (2,2)
if message [0] == '1':
    qc_alice.x(0)
if message [1] == '1':
    qc_alice.x(1)
qc_alice.h(1)
qc_alice.cx(1,0)
ket = Statevector(qc_alice)
ket.draw('latex')


# In[8]:


message = '11'
qc_alice = QuantumCircuit (2,2)
if message [0] == '1':
    qc_alice.x(0)
if message [1] == '1':
    qc_alice.x(1)
qc_alice.h(1)
qc_alice.cx(1,0)
ket = Statevector(qc_alice)
ket.draw('latex')


# In[ ]:


# Bob receives these states ( the state that alice coded) he needs to disentangle them
qc_bob = QuantumCircuit (2,2)
qc_bob.cx(1,0)
qc_bob.h(1)
qc_bob.measure([0,1],[0,1])
qc_bob.draw()

Aer.get_backend('aer_simulator').run(qc_alice.compose(qc_bob)).result().get_counts()


# In[9]:


#Generalised bell_pair
def create_bell_pair():
    
    qc = QuantumCircuit(2)
    qc.h(1)
    qc.cx(1, 0)
    return qc


# In[10]:


#Generalised encoding
def encode_message(qc, qubit, msg):
    if len(msg) != 2 or not set(msg).issubset({"0","1"}):
        raise ValueError("message %s is invalid" %msg )
    if msg[1] == "1":
        qc.x(qubit)
    if msg[0] == "1":
        qc.z(qubit)
    return qc


# In[25]:


#Generalised decoding
def decode_message(qc):
    qc.cx(1, 0)
    qc.h(1)
    return qc


# In[26]:


# Charlie creates the entangled pair between Alice and Bob

qc = create_bell_pair()
qc.barrier()

# we want to send the message '10'. You can try changing this
message = '10'
qc = encode_message(qc, 1, message)
qc.barrier()

# Alice then sends her qubit to Bob.
qc = decode_message(qc)

# Finally, Bob measures his qubits to read Alice's message
qc.measure_all()

qc.draw()


# In[32]:


aer_sim = Aer.get_backend('aer_simulator')
qobj = assemble(qc)
result = aer_sim.run(qobj).result()
counts = result.get_counts(qc)
print(counts)
plot_histogram(counts)


# In[14]:


qc_charlie = QuantumCircuit(2,2)
qc_charlie.h(1)
qc_charlie.cx(1,0)
qc_charlie.draw()


MESSAGE = '01'
qc_alice = QuantumCircuit(2,2)
if MESSAGE[-2]=='1':
    qc_alice.z(1)
if MESSAGE[-1]=='1':
    qc_alice.x(1)
    
    
qc_bob = QuantumCircuit (2,2)
qc_bob.cx(1,0)
qc_bob.h(1)
qc_bob.measure([0,1],[0,1])
qc_bob.draw()

complete_qc = qc_charlie.compose(qc_alice.compose(qc_bob))
Aer.get_backend('aer_simulator').run(complete_qc).result().get_counts()


# In[ ]:


#Superdense Coding on a Real Quantum Computer

shots = 1024

IBMQ.load_account()

provider = IBMQ.get_provider(hub='ibm-q')
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2 
                                       and not x.configuration().simulator 
                                       and x.status().operational==True))
print("least busy backend: ", backend)

t_qc = transpile(qc, backend, optimization_level=3)
job = backend.run(t_qc)
result = job.result()
plot_histogram(result.get_counts(qc))


# In[ ]:




