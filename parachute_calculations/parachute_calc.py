#What does "clear,clc" mean?
#clear,clc

import numpy as n
from matplotlib import pyplot as p

#This section lays out the varibles that should be changed
Apogee = 4500 #ft
MainEjectHeight = 550 #ft
AirDensity = 0.00233546 #slug/ft^3 at 600 ft altitude


#This section is for rocket parameters
g = 32.2 #ft/s^2
NoseCone = 2.39/g #slugs
PayloadTube = 3.37/g #slugs
ForwardSwitchBand = 1.91/g #slugs
DrogueTube = 1.44/g #slugs
AvionicsBay = 4.42/g #slugs
MainTube = 1.96/g #slugs
AftSwitchBand = 1.71/g
ForwardMotorTube = 1.46/g #slugs
AftMotorTube = 3.14/g #slugs
MotorWeightNoProp = (5.77 - 2.8)/g #slugs

Section1 = NoseCone + PayloadTube + ForwardSwitchBand #slugs
Section2 = DrogueTube + AvionicsBay + MainTube #slugs
Section3 = ForwardMotorTube + AftMotorTube + AftSwitchBand + MotorWeightNoProp #slugs

RocketWeightNoM = (Section1 + Section2 + Section3) #slugs

#This section creates matrices with drogue and main 
#parachute options
#Parachute data taken from fruitychutes
#Main parachutes = Iris Ultra Standard Parachutes
#DrogueParachute = Elliptical/Compact Elliptical Parachutes

Drogue = [12, 15, 18, 24] #inches
DrogueCd = [1.6, 1.6, 1.6, 1.6]
Main = [36, 48, 60, 72, 84, 96, 120] #inches
MainCd = [2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2]

#"zeros" create matricies of zeros length and width of Main length and Drogue length
#Making the matrices to keep track of the data
#Parachutes = zeros(len(Main),len(Drogue)) 
Parachutes = n.zeros([len(Main), len(Drogue)])
VDrogue = n.zeros([len(Main), len(Drogue)])
VMain = n.zeros([len(Main), len(Drogue)])
KE1 = n.zeros([len(Main), len(Drogue)])
KE2 = n.zeros([len(Main), len(Drogue)])
KE3 = n.zeros([len(Main), len(Drogue)])
KE1V = n.zeros([len(Main), len(Drogue)])
KE2V = n.zeros([len(Main), len(Drogue)])
KE3V = n.zeros([len(Main), len(Drogue)])
DecentTime = n.zeros([len(Main), len(Drogue)])
#Drift0 = n.zeros([len(Main), len(Drogue)]) Drift0 is never used
Drift5 = n.zeros([len(Main), len(Drogue)])
Drift10 = n.zeros([len(Main), len(Drogue)])
Drift15 = n.zeros([len(Main), len(Drogue)])
Drift20 = n.zeros([len(Main), len(Drogue)])

#For loop to get data for all drogue and main configurations
for i in range (len(Main)):
    for j in range (len(Drogue)):
        Parachutes[i,j] = Drogue[j], " + ", Main[i]
        #Decent Velocities: Drogue & Main
        VDrogue[i,j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * 1.6 * (Drogue[j]/12)**2))
        #"1.6" previously DrogueCd[j]
        VMain[i,j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * 2.2 * (Main[i]/12)**2))
        #"2.2" previously "MainCd[i]"
        
        #Kinetic Energy Calculations
        KE1[i,j] = (.5) * (Section1) * (VMain[i,j]**2) #lbf
        KE2[i,j] = (.5) * (Section2) * (VMain[i,j]**2) #lbf #This is the important one
        KE3[i,j] = (.5) * (Section3) * (VMain[i,j]**2) #lbf
        
        #Kinetic energy calculations for the drogue
        KE1V[i,j] = (.5) * (Section1) * (VDrogue[i,j]**2) #lbf
        KE2V[i,j] = (.5) * (Section2) * (VDrogue[i,j]**2) #lbf #This is the important one
        KE3V[i,j] = (.5) * (Section3) * (VDrogue[i,j]**2) #lbf
        
        #Decent Time Calculations
        DecentTime[i,j] = ((Apogee - MainEjectHeight)/VDrogue[i,j]) + (MainEjectHeight/VMain[i,j]) #s
        
        #Drift Calculations
        #Drift0[i,j] = (0) * (DecentTime[i,j]) #ft #Constantly defined as 0, not referenced after this line
        Drift5[i,j] = (7 + 1/3) * (DecentTime[i,j]) #ft
        Drift10[i,j] = (14 + 2/3) * (DecentTime[i,j]) #ft
        Drift15[i,j] = (22) * (DecentTime[i,j]) #ft
        Drift20[i,j] = (29 + 1/3) * (DecentTime[i,j]) #ft #This is the important one


#Figure to show the drogue decent velocities
'''figure(1)
bar(Drogue, VDrogue(1,:))
title('Drogue Parachute Decent Velocities')
xlabel('Drogue Diameter (in)')
ylabel('Velocity (ft/s)')'''

def drogue_decent_velocity():
    p.plot(Drogue, VDrogue)
    p.title('Drogue Parachute Decent Velocities')
    p.xlabel('Drogue Diameter (in)')
    p.ylabel('Velocity (ft/s)')

#Figure to show the Main decent velocities
'''figure(2)
bar(Main, VMain(:,1))
title('Main Parachute Decent Velocities')
xlabel('Main Diameter (in)')
ylabel('Velocity (ft/s)')'''

def main_decent_velocity():
    p.plot(Main, VMain)
    p.title('Drogue Parachute Decent Velocities')
    p.xlabel('Drogue Diameter (in)')
    p.ylabel('Velocity (ft/s)')

#Figure to show the ground hit kinetic energy for each main parachute
#Section 1
'''figure(3)
bar(Main, KE2(:,1))
title('Ground Hit Kinetic Energy of Section 2')
xlabel('Main Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

########################################################################################################################

def main_ground_hit_kinetic_1():
    p.plot(Main, KE1)
    p.title('Ground Hit Kinetic Energy of Section 1 for Main')
    p.xlabel('Main Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

#Figure to show the ground hit kinetic energy for each main parachute
#Section 2
'''figure(9)
bar(Main, KE1(:,1))
title('Ground Hit Kinetic Energy of Section 1')
xlabel('Main Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

def main_ground_hit_kinetic_2():
    p.plot(Main, KE2)
    p.title('Ground Hit Kinetic Energy of Section 2 for Main')
    p.xlabel('Main Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

#Figure to show the ground hit kinetic energy for each main parachute
#Section 3
'''figure(10)
bar(Main, KE3(:,1))
title('Ground Hit Kinetic Energy of Section 3')
xlabel('Main Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

def main_ground_hit_kinetic_3():
    p.plot(Main, KE3)
    p.title('Ground Hit Kinetic Energy of Section 3 for Main')
    p.xlabel('Main Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

########################################################################################################################   

#Figure to show the ground hit kinetic energy for each drogue parachute for
#section 1
'''figure(6)
bar(Drogue, KE1V(1, :))
title('Ground Hit Kinetic Energy of Section 1 for Drogue')
xlabel('Drogue Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

def drogue_ground_hit_kinetic_1():
    p.plot(Drogue, KE1V)
    p.title('Ground Hit Kinetic Energy of Section 1 for Drogue')
    p.xlabel('Drogue Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

#Figure to show the ground hit kinetic energy for each drogue parachute for
#section 2
'''figure(7)
bar(Drogue, KE2V(1, :))
title('Ground Hit Kinetic Energy of Section 2 for Drogue')
xlabel('Drogue Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

def drogue_ground_hit_kinetic_2():
    p.plot(Drogue, KE2V)
    p.title('Ground Hit Kinetic Energy of Section 2 for Drogue')
    p.xlabel('Drogue Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

#Figure to show the ground hit kinetic energy for each drogue parachute for
#section 3
'''figure(8)
bar(Drogue, KE3V(1, :))
title('Ground Hit Kinetic Energy of Section 3 for Drogue')
xlabel('Drogue Diameter (in)')
ylabel('Kinetic Energy (lbf)')'''

def drogue_ground_hit_kinetic_3():
    p.plot(Drogue, KE3V)
    p.title('Ground Hit Kinetic Energy of Section 3 for Drogue')
    p.xlabel('Drogue Diameter (in)')
    p.ylabel('Kinetic Energy (lbf)')

########################################################################################################################

#Figure to show the decent time for each drogue-main configuration
'''figure(4)
bar(Main, DecentTime)
legend('12','15','18','24')
title('Decent Time for Different Configurations')
xlabel('Parachute Configuration')
ylabel('Time (s)')'''

def decent_time():
    p.plot(Main, DecentTime)
    p.legend('12','15','18','24')
    p.title('Decent Time for Different Configurations')
    p.xlabel('Parachute Configuration')
    p.ylabel('Time (s)')

#Figure to show the drift for each drogue-main configuration
'''figure(5)
bar(Main, Drift20)
legend('12','15','18','24')
title('20 mi/hr Drift for Different Configurations')
xlabel('Parachute Configuration')
ylabel('Drift (ft)')'''

def drift():
    p.plot(Main, Drift20)
    p.legend('12','15','18','24')
    p.title('20 mi/hr Drift for Different Configurations')
    p.xlabel('Parachute Configuration')
    p.ylabel('Drift (ft)')

#Prints out all of the drogue-main configurations that meet the NASA handbook requirements:

print('NASA Handbook Successful Parachute Configurations')
for i in range(len(Main)):
    for j in range(len(Drogue)):
        if(KE2[i,j] < 75 and DecentTime[i,j] < 90 and Drift20[i,j] < 2500):
            print('Drogue Parachute #d in and Main Parachute #d in\n', Drogue(j), Main(i))

#Prints out all of the drogue-main parachute configurations that meet both
#the NASA handbook requirements and CyLaunch's requirements 
#These are the configurations that should be used

print('\n')
print('CyLaunch Successful Parachute Configurations')

for i in range (len(Main)):
    for j in range (len(Drogue)):
        if(KE2[i,j] < 75 and DecentTime[i,j] < 90 and Drift20[i,j] < 2500 and VDrogue[i,j] < 100 and VMain[i,j] < 15):
            print('Drogue Parachute #d in and Main Parachute #d in\n', Drogue[j], Main[i])


#Are these points on a graph we want printed? (below)  
#Drift0(5,3)
#Drift5(5,3)
#Drift10(5,3)
#Drift15(5,3)
#Drift20(5,3)
