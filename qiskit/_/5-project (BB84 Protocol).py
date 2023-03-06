#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Quantum Key Distribution (BB84 Protocol)


# In[4]:


from qiskit import *
import random
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np


# In[3]:


#1-encode
key_length = 500
random.seed(0)
alice_bits = ""
for key in range(key_length):
    randBit = random.randint(0, 1) 
    randBit = str(randBit)
    alice_bits =  alice_bits + randBit
    
print("The bits Alice is going to send are: %s... " % alice_bits[:50] )


# In[4]:


def generate_random_bases(num_of_bases):
    bases_string = ""
    for i in range(num_of_bases):
        randBasis = random.randint(0, 1) 
        if randBasis == 0:
            bases_string += "Z" 
        else:
            bases_string += "X"       
    return bases_string
alice_bases = generate_random_bases(key_length) 
print("The bases Alice is going to encode them in are: %s... " %alice_bases[:50])


# In[5]:


#  X basis -> |+> and |->  , Z basis -> |0> and |1>

def encode(bits, bases):
    encoded_qubits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit=="0" and basis == "Z":
            encoded_qubits.append(qc) 
        elif bit=="1" and basis == "Z":
            qc.x(0)
            encoded_qubits.append(qc)
        elif bit=="0" and basis == "X":
            qc.h(0) 
            encoded_qubits.append(qc)
        elif bit=="1" and basis == "X":
            qc.x(0) 
            qc.h(0) 
            encoded_qubits.append(qc)
    return (encoded_qubits)

encoded_qubits = encode(alice_bits, alice_bases)

for i in range(5):    # Print circuits for first 5 qubits.
    print(encoded_qubits[i])
print("etc")


# In[6]:


# 2-Sending the qubits
QUANTUM_CHANNEL = encoded_qubits


# In[7]:


#3- Bob measurement
bob_bases = generate_random_bases(key_length) 
print("The bases Bob is going to decode them in are: %s... " %bob_bases[:50])


# In[8]:


def measure(qubits, bases):
        bits = ""       # The results of measurements
        for qubit, basis in zip(qubits, bases):
            if basis == "Z":
                qubit.measure(0, 0)
            elif basis == "X":
                qubit.h(0)
                qubit.measure(0, 0)
                
            simulator = Aer.get_backend('qasm_simulator')
            result = execute(qubit, backend=simulator, shots=1).result().get_counts()
            measured_bit = max(result, key=result.get) 
            
            bits = bits + measured_bit
            
        return bits
    
qubits_received = QUANTUM_CHANNEL
bob_bits = measure(qubits_received, bob_bases)
print("The first few bits Bob received are: %s... "  %bob_bits[:10] )


# In[9]:


#4-Comparison
CLASSICAL_CHANNEL = alice_bases 


# In[13]:


list_common_bases = []
for i in range(key_length):
    if alice_bases [i] == bob_bases[i]:
        list_common_bases.append(i)

print("The indices of the first 10 bases they share in common are: %s " %list_common_bases[:10] )


# In[14]:


# Bob can discard all the rest of the bits, and only keep the ones that were measured in the same bases.
list_common_bob_bit = []
for index in list_common_bases:
    bob_bit = bob_bits[index]
    list_common_bob_bit.append(bob_bit)
    
print(" Bob bits with common bases :%s" %list_common_bob_bit)


# In[15]:


CLASSICAL_CHANNEL = list_common_bases  # Bob tells Alice which bases they shared in common


# In[16]:


# Alice keeps only the bits they shared in common
list_common_alice_bit = []
for index in list_common_bases:
    alice_bit = alice_bits[index]
    list_common_alice_bit.append(alice_bit)
    
print(" Bob bits with common bases :%s" %list_common_alice_bit)


# In[17]:


if list_common_alice_bit[:100] == list_common_bob_bit[:100]:
    print("Yep, Alice and Bob seem to have the same bits!")
else:
    print("Uh oh, at least one of the bits is different.")


# In[18]:


# they need to discard the first 100 bits, since Eve may have been listening in on the classical channel
list_common_alice_bit = list_common_alice_bit [100:]
list_common_bob_bit = list_common_bob_bit [100:]


# In[28]:


key = "" 
for bit in alice_bits:  # Or bob_bits, since both should be the same
    key = key + bit

print('''Shhhhh, the key is:
%s
Don't tell anyone!''' %key)
print("\nThe key is %s bits long." %len(key))


# In[29]:


#5-Interception
alice_bits = ""
for i in range(key_length):
    randBit = random.randint(0, 1) 
    alice_bits += str(randBit) 
    
alice_bases = generate_random_bases(key_length)

encoded_qubits = encode(alice_bits, alice_bases)

QUANTUM_CHANNEL = encoded_qubits


# In[30]:


qubits_intercepted = QUANTUM_CHANNEL 
eve_bases = generate_random_bases(key_length)
eve_bits = measure(qubits_intercepted, eve_bases) 


# In[31]:


#Because of the No-Cloning Theorem of Quantum Mechanics,Eve cannot copy the qubits from the quantum channel
# Eve encodes her decoy qubits and sends them along the quantum channel
QUANTUM_CHANNEL = encode(eve_bits, eve_bases)


# In[33]:


# Bob doesn't know that Eve has intercepted them yet.
bob_bases = generate_random_bases(key_length)
qubits_received = QUANTUM_CHANNEL    # Receive qubits from quantum channel
bob_bits = measure(qubits_received, bob_bases)


# In[34]:


#Comparison
CLASSICAL_CHANNEL = alice_bases


# In[37]:


list_common_bases = []
for i in range(key_length):
    if alice_bases [i] == bob_bases[i]:
        list_common_bases.append(i)

print("The indices of the first 10 bases they share in common are: %s " %list_common_bases[:10] )

list_common_bob_bit = []
for index in list_common_bases:
    bob_bit = bob_bits[index]
    list_common_bob_bit.append(bob_bit)
    
print("\n Bob bits with common bases :%s" %list_common_bob_bit)


# In[38]:


CLASSICAL_CHANNEL = list_common_bases

list_common_alice_bit = []
for index in list_common_bases:
    alice_bit = alice_bits[index]
    list_common_alice_bit.append(alice_bit)
    
print(" Bob bits with common bases :%s" %list_common_alice_bit)


# In[39]:


if list_common_alice_bit[:100] == list_common_bob_bit[:100]:
    print("Yep, Alice and Bob seem to have the same bits!")
else:
    print("Uh oh, at least one of the bits is different.")


# In[1]:


#After comparing the first 100 bits, they see that their bits don't match! 


# In[2]:


#Example_2


# In[6]:


np.random.seed(seed=0)
n = 100

## Step 1
#Alice generates bits
alice_bits = randint(2, size=n)
print(alice_bits)


# In[7]:


def encode_message(bits, bases):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: 
            if bits[i] == 0:
                pass 
            else:
                qc.x(0)
        else: 
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message


# In[8]:


np.random.seed(seed=0)
n = 100

## Step 1
alice_bits = randint(2, size=n)

## Step 2
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)


# In[9]:


print('bit = %i' % alice_bits[0])
print('basis = %i' % alice_bases[0])


# In[10]:


message[0].draw()


# In[11]:


print('bit = %i' % alice_bits[4])
print('basis = %i' % alice_bases[4])
message[4].draw()


# In[12]:


## Step 3
bob_bases = randint(2, size=n)
print(bob_bases)


# In[13]:


def measure_message(message, bases):
    backend = Aer.get_backend('aer_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0: 
            message[q].measure(0,0)
        if bases[q] == 1: 
            message[q].h(0)
            message[q].measure(0,0)
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements


# In[14]:


np.random.seed(seed=0)
n = 100

## Step 1
alice_bits = randint(2, size=n)

## Step 2
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)

## Step 3
bob_bases = randint(2, size=n)
bob_results = measure_message(message, bob_bases)


# In[15]:


message[0].draw()


# In[16]:


message[6].draw()


# In[17]:


print(bob_results)


# In[18]:


def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            good_bits.append(bits[q])
    return good_bits


# In[19]:


np.random.seed(seed=0)
n = 100

## Step 1
alice_bits = randint(2, size=n)

## Step 2
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)

## Step 3
bob_bases = randint(2, size=n)
bob_results = measure_message(message, bob_bases)

## Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
print(alice_key)


# In[20]:


np.random.seed(seed=0)
n = 100

## Step 1
alice_bits = randint(2, size=n)

## Step 2
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)

## Step 3
bob_bases = randint(2, size=n)
bob_results = measure_message(message, bob_bases)

## Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)
print(bob_key)


# In[25]:


np.random.seed(seed=0)
n = 100

## Step 1
# Alice generates bits
alice_bits = randint(2, size=n)

## Step 2
# Create an array to tell us which qubits
# are encoded in which bases
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)

## Step 3
# Decide which basis to measure in:
bob_bases = randint(2, size=n)
bob_results = measure_message(message, bob_bases)

## Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)

## Step 5
sample_size = 15
bit_selection = randint(n, size=sample_size)

bob_sample = sample_bits(bob_key, bit_selection)
print("  bob_sample = " + str(bob_sample))
alice_sample = sample_bits(alice_key, bit_selection)
print("alice_sample = "+ str(alice_sample))


# In[26]:


bob_sample == alice_sample


# In[27]:


print(bob_key)
print(alice_key)
print("key length = %i" % len(alice_key))


# In[ ]:




