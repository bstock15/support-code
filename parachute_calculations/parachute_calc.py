#-----------------------------------------------------------------
# rvw - put a high level description of the software in this file
#-----------------------------------------------------------------
import numpy as n
from matplotlib import pyplot as p

def Main():
    #-------------------------------------------------------------
    # Constants
    #-------------------------------------------------------------
    g = 32.2 #ft/s^2

    #-------------------------------------------------------------
    # Rocket Performance Parameters
    #-------------------------------------------------------------
    Apogee = 4500 #ft
    MainEjectHeight = 550 #ft
    AirDensity = 0.00233546 #slug/ft^3 at 600 ft altitude

    #-------------------------------------------------------------
    # Rocket Mass Parameters
    #-------------------------------------------------------------
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

    #-------------------------------------------------------------
    # Rocket Success Parameters
    #-------------------------------------------------------------
    KE2_Limit = 75 # rvw - Add units
    DecentTime_Limit = 90
    Drift20_Limit = 2500
    VDrogue_Limit = 100
    VMain_Limit = 15

    Section1 = NoseCone + PayloadTube + ForwardSwitchBand #slugs
    Section2 = DrogueTube + AvionicsBay + MainTube #slugs
    Section3 = ForwardMotorTube + AftMotorTube + AftSwitchBand + MotorWeightNoProp #slugs

    RocketWeightNoM = (Section1 + Section2 + Section3) #slugs

    # Parachute data taken from fruitychutes
    # Main parachutes = Iris Ultra Standard Parachutes
    # DrogueParachute = Elliptical/Compact Elliptical Parachutes

    DrogueCd = [1.6, 1.6, 1.6, 1.6]
    Drogue = [12, 15, 18, 24]
    VDrogue = [0, 0, 0, 0] 
    Main = [36, 48, 60, 72, 84, 96, 120]
    MainCd = [2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2]
    VMain = [0, 0, 0, 0, 0, 0, 0]
    
    KE1 = [0, 0, 0, 0, 0, 0, 0]
    KE2 = [0, 0, 0, 0, 0, 0, 0]
    KE3 = [0, 0, 0, 0, 0, 0, 0]
    
    KE1V = [0, 0, 0, 0]
    KE2V = [0, 0, 0, 0]
    KE3V = [0, 0, 0, 0]

    DecentTime = n.zeros([len(Main), len(Drogue)])
    Drift0 = n.zeros([len(Main), len(Drogue)]) 
    Drift5 = n.zeros([len(Main), len(Drogue)])
    Drift10 = n.zeros([len(Main), len(Drogue)])
    Drift15 = n.zeros([len(Main), len(Drogue)])
    Drift20 = n.zeros([len(Main), len(Drogue)])

    # rvw - take some time and tell me what each loop is doing in a comment
    # rvw - it's good practice to use i as the first layer of a for loop and go down with
    # each layer of nesting (i, j, k, etc).
    for j in range (len(Main)): 
        VMain[j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * MainCd[j] * (Main[j]/12)**2))             
        #Kinetic Energy Calculations
        KE1[j] = (.5) * (Section1) * (VMain[j]**2) #lbf
        KE2[j] = (.5) * (Section2) * (VMain[j]**2) #lbf #This is the important one
        KE3[j] = (.5) * (Section3) * (VMain[j]**2) #lbf       
        
    for j in range (len(Drogue)):
        VDrogue[j] = n.sqrt((8 * RocketWeightNoM * g)/(n.pi * AirDensity * DrogueCd[j] * (Drogue[j]/12)**2))
        #Kinetic Energy Calculations
        KE1V[j] = (.5) * (Section1) * (VDrogue[j]**2) #lbf
        KE2V[j] = (.5) * (Section2) * (VDrogue[j]**2) #lbf #This is the important one
        KE3V[j] = (.5) * (Section3) * (VDrogue[j]**2) #lbf

    for i in range(len(Main)):
        for j in range (len(Drogue)):     
                DecentTime[i,j] = ((Apogee - MainEjectHeight)/VDrogue[j]) + (MainEjectHeight/VMain[i]) #s       
                #Drift Calculations
                # rvw - unless it slows down the progam a ton, lets go ahead and get this data.
                # we can cross refrence it with successful configurations to get more data
                '''Drift0[i,j] = (0) * (DecentTime[i,j]) #ft 
                Drift5[i,j] = (7 + 1/3) * (DecentTime[i,j]) #ft
                Drift10[i,j] = (14 + 2/3) * (DecentTime[i,j]) #ft
                Drift15[i,j] = (22) * (DecentTime[i,j]) #ft'''
                Drift20[i,j] = (29 + 1/3) * (DecentTime[i,j]) #ft #This is the important one

    # Prints out all of the drogue-main configurations that meet the NASA handbook requirements 3.3, 3.12, 3.11
    print('\n')
    print('NASA Handbook Successful Parachute Configurations:')
    for i in range(len(Main)):
        for j in range(len(Drogue)):
            if(KE2[j] < KE2_Limit and DecentTime[i,j] < DecentTime_Limit and Drift20[i,j] < Drift20_Limit):
                data = n.array(["Drogue:", Drogue[j] , "Main:", Main[i]])
                print(data) # rvw - we'll want to print outside of the loop, otherwise we're printing the entire array
                            # each time this if statement is hit

    #Prints out all of the drogue-main parachute configurations that meet both
    #the NASA handbook requirements and CyLaunch's requirements 
    #These are the configurations that should be used

    print('\n')
    print('CyLaunch Successful Parachute Configurations:')
    # rvw - we now have an array of rockets that meet nasa configurations, why don't we iterate through that list instead of all rockets?
    for i in range (len(Main)):
        for j in range (len(Drogue)):
            if(KE2[j] < KE2_Limit and DecentTime[i,j] < DecentTime_Limit and Drift20[i,j] < Drift20_Limit and VDrogue[j] < VDrogue_Limit and VMain[j] < VMain_Limit):
                data2 = n.array(["Drogue:", Drogue[j] , "Main:", Main[i]])
                print(data2) # rvw - same as above

    graph_data(1, Drogue, VDrogue, Drogue, 1, 'Drogue Parachute Decent Velocities', 'Drogue Diameter (in)', 'Velocity (ft/s)')

    graph_data(2, Main, VMain, Main, 3, 'Main Parachute Decent Velocities', 'Main Diameter (in)', 'Velocity (ft/s)')

    graph_data(3, Main, KE1, Main, 3, 'Ground Hit Kinetic Energy of Section 1 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(4, Main, KE2, Main, 3, 'Ground Hit Kinetic Energy of Section 2 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(5, Main, KE3, Main, 3, 'Ground Hit Kinetic Energy of Section 3 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(6, Drogue, KE1V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 1 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(7, Drogue, KE2V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 2 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(8, Drogue, KE3V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 3 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data2(9, Main, DecentTime, ('12','15','18','24'), 'Decent Time for Different Configurations', 'Main Diameter (in)', 'Time (s)')

    graph_data2(10, Main, Drift20, ('12','15','18','24'), '20 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')

    # rvw - can we make a graph for each drift scenario for each successful rocket config?
    
def graph_data(figure, x, y, z, c, title, xlabel, ylabel):
    p.figure(figure)
    p.bar(x, y, width = c)
    p.xticks(z)
    p.yticks(y)
    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)
    p.grid()
    p.show()

def graph_data2(figure, x, y, legend, title, xlabel, ylabel):
    p.figure(figure)
    p.plot(x, y)
    p.legend(legend, title = "Drogue Diameter (in)")
    p.title(title)
    p.xlabel(xlabel)
    p.ylabel(ylabel)
    p.grid()
    p.show()

if __name__ == "__main__":
    Main()

#Drift0(5,3)
#Drift5(5,3)
#Drift10(5,3)
#Drift15(5,3)
#Drift20(5,3)