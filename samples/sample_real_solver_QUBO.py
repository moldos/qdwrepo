#problem: find min(a+b+c=1)
#we square it for QUBO => E(a,b,c)=(a+b+c-1)**2
#have in mind that a**2=b**2=c**2=1
#=>E=2ab+2ac+2bc-a-b-c+1 
#=> f=2x0x1+2x0x2+2x1x2-x0-x1-x2+1
#STEP 2 - coupler mapping
#because of chimera architecture we have to use 
# a -> q4 cu bias = -1
# c -> q1 cu bias = -1
# b -> q0 and q5
# pt ca b=q0=q5 => we bias with -0.5
# we set couplig for q0-q5 as -3 (>2 - rest of the couplers)
# we have to compensate q0-q5=-3 via bias of q0,q5 =>
# => +bias of q0=q5 cu +1.5
#STEP 3
# we normalize the entire graph dividing by 3
# =>
# bias q4=q1=-0.33 and q0=q5=(-0.5+1.5)/3=0.33
# coupler q14=q04=q15=2/3=0.667 and q05=-3/3=-1
from dwave.system.samplers import DWaveSampler
#check the status of the qubits
print('valid_nodes=',DWaveSampler().nodelist[0:8])
#solve
qubit_biases={(0,0):0.333,(1,1):-0.333,(4,4):-0.333,(5,5):0.333}
coupler_strengths={(0,4):0.667,(1,4):0.667,(1,5):0.667,(0,5):-1.}
Q=dict(qubit_biases)
Q.update(coupler_strengths)
#sample once on DWave
response=DWaveSampler().sample_qubo(Q, num_reads=1)
print('response=',next(response.samples()))
response=DWaveSampler().sample_qubo(Q, num_reads=1000)
for (sample,energy,num) in response.data():
    print('answ=',sample,'Energy=',energy,'Occurences=',num)