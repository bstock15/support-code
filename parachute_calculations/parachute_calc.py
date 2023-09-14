import numpy as n
from matplotlib import pyplot as p

def Main():
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

    #Matrices to keep track of the data
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
    Drift0 = n.zeros([len(Main), len(Drogue)]) 
    Drift5 = n.zeros([len(Main), len(Drogue)])
    Drift10 = n.zeros([len(Main), len(Drogue)])
    Drift15 = n.zeros([len(Main), len(Drogue)])
    Drift20 = n.zeros([len(Main), len(Drogue)])

    #For loop to get data for all drogue and main configurations
    for i in range (len(Main)):
        for j in range (len(Drogue)):
            #Parachutes[i,j] = Drogue[j], " + ", Main[i] 
            Parachutes[i] = Main[i]
            Parachutes[j] = Drogue[j]

            #Decent Velocities: Drogue & Main
            VDrogue[i,j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * DrogueCd[j] * (Drogue[j]/12)**2))
            VMain[i,j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * MainCd[i] * (Main[i]/12)**2))       
            
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
            Drift0[i,j] = (0) * (DecentTime[i,j]) #ft 
            Drift5[i,j] = (7 + 1/3) * (DecentTime[i,j]) #ft
            Drift10[i,j] = (14 + 2/3) * (DecentTime[i,j]) #ft
            Drift15[i,j] = (22) * (DecentTime[i,j]) #ft
            Drift20[i,j] = (29 + 1/3) * (DecentTime[i,j]) #ft #This is the important one

    #Prints out all of the drogue-main configurations that meet the NASA handbook requirements
    print('\n')
    print('NASA Handbook Successful Parachute Configurations:')
    for i in range(len(Main)):
        for j in range(len(Drogue)):
            if(KE2[i,j] < 75 and DecentTime[i,j] < 90 and Drift20[i,j] < 2500):
                print('Drogue Parachute %d in and Main Parachute %d in\n', "Drogue:", Drogue[j], "Main:", Main[i])

    #Prints out all of the drogue-main parachute configurations that meet both
    #the NASA handbook requirements and CyLaunch's requirements 
    #These are the configurations that should be used

    print('\n')
    print('CyLaunch Successful Parachute Configurations:')
    for i in range (len(Main)):
        for j in range (len(Drogue)):
            if(KE2[i,j] < 75 and DecentTime[i,j] < 90 and Drift20[i,j] < 2500 and VDrogue[i,j] < 100 and VMain[i,j] < 15):
                print('Drogue Parachute %d in and Main Parachute %d in:\n', "Drogue:", Drogue[j], "Main:", Main[i])

    graph_data(1, Drogue, VDrogue, 'Drogue Parachute Decent Velocities', 'Drogue Diameter (in)', 'Velocity (ft/s)')

    graph_data(2, Main, VMain, 'Main Parachute Decent Velocities', 'Main Diameter (in)', 'Velocity (ft/s)')

    graph_data(3, Main, KE1, 'Ground Hit Kinetic Energy of Section 1 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(4, Main, KE2, 'Ground Hit Kinetic Energy of Section 2 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(5, Main, KE3, 'Ground Hit Kinetic Energy of Section 3 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(6, Drogue, KE1V, 'Ground Hit Kinetic Energy of Section 1 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(7, Drogue, KE2V, 'Ground Hit Kinetic Energy of Section 2 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(8, Drogue, KE3V, 'Ground Hit Kinetic Energy of Section 3 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data2(9, Main, DecentTime, ('12','15','18','24'),'Decent Time for Different Configurations', 'Parachute Configuration', 'Time (s)')

    graph_data2(10, Main, Drift20, ('12','15','18','24'),'20 mi/hr Drift for Different Configurations', 'Parachute Configuration', 'Drift (ft)')

    print('\n')
    print("Done")

def graph_data(figure, x, y, title, xlabel, ylabel):
    p.figure(figure)
    p.plot(x)
    p.plot(y)
    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)
    p.show()

def graph_data2(figure, x, y, legend, title, xlabel, ylabel):
    p.figure(figure)
    p.plot(x)
    p.plot(y)
    p.legend(legend)
    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)
    p.show()

if __name__ == "__main__":
    Main()

#Drift0(5,3)
#Drift5(5,3)
#Drift10(5,3)
#Drift15(5,3)
#Drift20(5,3)
