#!/usr/bin/env python
# coding: utf-8

# In[10]:


import random
import matplotlib.pyplot as plt

# Σταθερές
N = 8 # number of nodes
W = 4 # number of channels
L = 4 # buffer capacity

Nodes = [0,1,2,3,4,5,6,7]
Wavelengths = [0,1,2,3]

# Μια λίστα destination_nodes από λίστες destinations για τον κάθε κόμβο i. 
# Η κάθε λίστα περιλαμβάνει όλους τους κόμβους εκτός από τον εαυτό του
destination_nodes=[] 
for i in Nodes:
    destinations = [x for x in Nodes if x != Nodes[i]]
    destination_nodes.append(destinations)

#Τα κανάλια στα οποία ακούνε οι receivers
Rec_channel = [0,0,1,1,2,2,3,3] 

# Φόρτος b
b = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8, 5.6, 6.4, 7.2, 8]  

# Πίνακας πιθανοτήτων l(=λ)
l_values = [] 
for i in range(len(b)):
    l_values.append(b[i]/N) # λ=b/N

# Τρέχω την προσομοίωση για διαφορετική πιθανόητα l
for l in l_values:
    # Αρχικοποιώ τις μεταβλητές 
    buffers = [[] for _ in range(N)] # Μια λίστα με N=8 λίστες buffers
    trans = []
    time = 0
    num_packets_sent = 0
    delays = []

    while time < 200000:
        #Δημιουργία πακέτων
        for i in Nodes:
            creation_probability = random.random()
            if creation_probability <= l:
                if len(buffers[i]) < L: # Αν η ουρά δεν είναι γεμάτη γίνεται δημιουργία πακέτου
                    destination = random.choice(destination_nodes[i]) # Τυχαία επιλογή destination
                    buffers[i].append((destination, time)) # Αποθηκεύεται ο κόμβος προορισμού και η ώρα δημιουργίας πακέτου σε tuple  μορφής (destination node, time of packet creation)
        
        # Αρχικοποιήσεις πινάκων για transmission schedule
        Omega = Wavelengths.copy() # Λίστα των available channels
        A = Nodes.copy() # Λίστα των available Nodes 
        trans = [-1]*N # Αρχικοποίηση του trans, αν ο κόμβος i έχει trans[i]=-1 τότε δεν στέλνει σε κανένα μήκος κύματος 
        
        # Δημιουργία transmission schedule
        for i in range(W): # Tρέχει για 4 φορές όσο το πλήθος W των καναλιών
            if len(Omega)!=0: # Αν το μήκος της λίστας!=0, τότε υπάρχουν διαθέσιμα κανάλια
                k = random.choice(Omega) # Διαλέγουμε τυχαία ένα κανάλι k
                random_node = random.choice(A) # Διαλέγουμε τυχαία έναν κόμβο να μεταδόσει στο k
                trans[random_node] = k # Η θέση της λίστας trans είναι ο κόμβος και η τιμή του είναι το k
                A.remove(random_node)
                Omega.remove(k)
            else:
                break    
                
        # Αποστολή πακέτων
        for i in range(N): 
            for j in buffers[i]: # Ελέγχω όλα τα destinations (j) που υπάρχουν στον buffer του i
                if Rec_channel[j[0]]==trans[i]: # Αν το κανάλι του receiver του destination j[0] του κόμβου i είναι ίσο με το κανάλι του trans[i] τότε γίνεται αποστολή
                    delays.append(time - j[1]) # Για να βρω την καθυστέρηση αφαιρώ από τον τωρινό χρόνο την άφιξη j[1]
                    buffers[i].remove(j) # Αφαίρεση του προορισμού από τον buffer του κόμβου i
                    num_packets_sent+=1
                    break
        time += 1
        
    # Υπολογισμός Throughput και Delay    
    throughput=num_packets_sent/time
    delay=sum(delays)/num_packets_sent
    
    # Προσθέτει τα αποτελέσματα αυτού του γύρου στο plot
    plt.scatter(throughput, delay, label=f"l = {l}")

# Εμφάνιση γραφήματος
plt.xlabel('Throughput')
plt.ylabel('Delay')
plt.title('Throughput vs. Delay')
plt.legend()
plt.show()


# In[ ]:





# In[ ]:




