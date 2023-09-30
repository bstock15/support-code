# -----------------------------------------------------------------
# PROGRAM OVERVIEW:
# This program calculates the configurations of our Main and Drogue parachutes that are successful by NASA handbook, and CyLaunch, standards.
# This information is printed to the terminal in a grid form. The variables measured to calculate a succesful
# parachute combination are the kinetic energy the rocket impacts the ground with (in lbf), the decent time of the rocket (in seconds), 
# the number of feet (ft) the rocket drifts before impacting the ground, and the decent velocities of the Main and Drogue parachutes (in ft/s). 
# 
# This program also prints graphs displaying the decent velocities of the Main and Drogue parachutes, the kinetic energy the rocket impacts
# the ground with for all three sections of the rocket considering all the different combinations of both the Main and Drogue parachutes,
# the decent time given different parachute configurations, and the amount of drfit the rocket experiences with different parachute cofigurations
# while experiencing different wind speeds. 
# 
# TECHNICAL ANALYSIS:
# To calculate the values for kinetic energy upon ground impact, decent time, drift, and parachute velocites, various constants related to 
# the mass of rocket components and rocket performance parameters are defined before running any calculations. Empty arrays are then created to 
# store the information for each subsequent varible we calculate. The program then calculates values for each aforementioned variable using the 
# constants provided entered into equations. The variable values are stored into the empty arrays created at the beginning of the program using
# single or double For loops. Another two sets of For loops are then used to determine which combinations of parachutes meet our standards, 
# determined by the rocket success parameters. Finally, two functions outside of Main are used to create graphs of every relevant measurement
# in bar and line graph forms. 
# -----------------------------------------------------------------
import numpy as n
from matplotlib import pyplot as p

def Main():
    # -------------------------------------------------------------
    # Constants
    # -------------------------------------------------------------
    g = 32.2 # ft/s^2

    # -------------------------------------------------------------
    # Rocket Performance Parameters
    # -------------------------------------------------------------
    Apogee = 4500 # ft
    MainEjectHeight = 550 # ft
    PayloadEjectHeight = 500 # ft
    AirDensity = 0.00233546 # slug/ft^3 at 600 ft altitude

    # -------------------------------------------------------------
    # Rocket Mass Parameters
    # -------------------------------------------------------------
    NoseCone = 2.39/g # slugs
    PayloadTube = 3.37/g # slugs
    Payload = 5.00/g # slugs
    ForwardSwitchBand = 1.91/g # slugs
    DrogueTube = 1.44/g # slugs
    AvionicsBay = 4.42/g # slugs
    MainTube = 1.96/g # slugs
    AftSwitchBand = 1.71/g
    ForwardMotorTube = 1.46/g # slugs
    AftMotorTube = 3.14/g # slugs
    MotorWeightNoProp = (5.77 - 2.8)/g # slugs

    # -------------------------------------------------------------
    # Rocket Success Parameters
    # -------------------------------------------------------------
    KE2_Limit_lbf = 75 # lbf
    DecentTime_Limit_s = 90 # seconds
    Drift20_Limit_ft = 2500 # ft
    VDrogue_Limit_fts= 100 # ft/s
    VMain_Limit_fts = 15 # ft/s

    Section1i = NoseCone + PayloadTube + Payload + ForwardSwitchBand # slugs
    Section1f = PayloadTube + ForwardSwitchBand # slugs
    Section2 = DrogueTube + AvionicsBay + MainTube # slugs
    Section3 = ForwardMotorTube + AftMotorTube + AftSwitchBand + MotorWeightNoProp # slugs

    RocketWeightNoMi = (Section1i + Section2 + Section3) # slugs
    RocketWeightNoMf = (Section1f + Section2 + Section3) # slugs

    # Parachute data taken from fruitychutes
    # Main parachutes = Iris Ultra Standard Parachutes
    # DrogueParachute = Elliptical/Compact Elliptical Parachutes

    DrogueCd = [1.6, 1.6, 1.6, 1.6]
    Drogue = [12, 15, 18, 24]
    VDrogue = [0, 0, 0, 0] 
    Main = [36, 48, 60, 72, 84, 96, 120]
    MainCd = [2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2]
    VMaini = [0, 0, 0, 0, 0, 0, 0]
    VMainf = [0, 0, 0, 0, 0, 0, 0]
    
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

    # Calculates Main parachute decent velocities
    # and the respective ground hit kinetic energy measurements on all three sections of the rocket
    for i in range (len(Main)): 
        # Main Parachute Descent Velocity Calculations
        VMaini[i] = n.sqrt((8 * RocketWeightNoMi * g)/(n.pi * AirDensity * MainCd[i] * (Main[i]/12)**2))
        VMainf[i] = n.sqrt((8 * RocketWeightNoMf * g)/(n.pi * AirDensity * MainCd[i] * (Main[i]/12)**2))
        # Kinetic Energy Calculations
        KE1[i] = (.5) * (Section1f) * (VMainf[i]**2) # lbf
        KE2[i] = (.5) * (Section2) * (VMainf[i]**2) # lbf This is the important one
        KE3[i] = (.5) * (Section3) * (VMainf[i]**2) # lbf       
        
    # Calculates Drogue parachute decent velocities 
    # and the respective ground hit kinetic energy measurements on all three sections of the rocket
    for i in range (len(Drogue)):
        VDrogue[i] = n.sqrt((8 * RocketWeightNoMi * g)/(n.pi * AirDensity * DrogueCd[i] * (Drogue[i]/12)**2))
        # Kinetic Energy Calculations
        KE1V[i] = (.5) * (Section1f) * (VDrogue[i]**2) # lbf
        KE2V[i] = (.5) * (Section2) * (VDrogue[i]**2) # lbf This is the important one
        KE3V[i] = (.5) * (Section3) * (VDrogue[i]**2) # lbf

    # Calculates the decent time of the rocket given different parachute configurations
    # and the distance, in ft, traveled after parachute deployment, given different constant wind speeds
    for i in range(len(Main)):
        for j in range (len(Drogue)):     
                DecentTime[i,j] = ((Apogee - MainEjectHeight)/VDrogue[j]) + ((MainEjectHeight - PayloadEjectHeight)/VMaini[i]) + (PayloadEjectHeight/VMainf[i]) # s       
                # Drift Calculations
                Drift0[i,j] = (0) * (DecentTime[i,j]) # ft 
                Drift5[i,j] = (7 + 1/3) * (DecentTime[i,j]) # ft
                Drift10[i,j] = (14 + 2/3) * (DecentTime[i,j]) # ft
                Drift15[i,j] = (22) * (DecentTime[i,j]) # ft
                Drift20[i,j] = (29 + 1/3) * (DecentTime[i,j]) # ft This is the important one

    # Prints out all of the drogue-main configurations that meet the NASA handbook requirements 3.3, 3.12, 3.11
    print('\n')
    print('NASA Handbook Successful Parachute Configurations:')
    for i in range(len(Main)):
        for j in range(len(Drogue)):
            if(KE2[j] < KE2_Limit_lbf and DecentTime[i,j] < DecentTime_Limit_s and Drift20[i,j] < Drift20_Limit_ft):
                data = n.array(["Drogue:", Drogue[j] , "Main:", Main[i]])            
                print(data)                       

    # Prints out all of the drogue-main parachute configurations that meet both
    # the NASA handbook requirements and CyLaunch's requirements 
    # These are the configurations that should be used

    print('\n')
    print('CyLaunch Successful Parachute Configurations:')
    for i in range (len(data)):
        if(KE2[j] < KE2_Limit_lbf and DecentTime[i,j] < DecentTime_Limit_s and Drift20[i,j] < Drift20_Limit_ft and VDrogue[j] < VDrogue_Limit_fts and VMaini[j] < VMain_Limit_fts):
            data2 = n.array(["Drogue:", Drogue[j] , "Main:", Main[i]])
            print(data2)

    graph_data(1, Drogue, VDrogue, Drogue, 1, 'Drogue Parachute Decent Velocities', 'Drogue Diameter (in)', 'Velocity (ft/s)')

    graph_data(2, Main, VMaini, Main, 3, 'Pre-Payload Ejection Main Parachute Decent Velocities', 'Main Diameter (in)', 'Velocity (ft/s)')

    graph_data(3, Main, VMainf, Main, 3, 'Post-Payload Ejection Main Parachute Decent Velocities', 'Main Diameter (in)', 'Velocity (ft/s)')

    graph_data(4, Main, KE1, Main, 3, 'Ground Hit Kinetic Energy of Section 1 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(5, Main, KE2, Main, 3, 'Ground Hit Kinetic Energy of Section 2 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(6, Main, KE3, Main, 3, 'Ground Hit Kinetic Energy of Section 3 for Main', 'Main Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(7, Drogue, KE1V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 1 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(8, Drogue, KE2V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 2 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data(9, Drogue, KE3V, Drogue, 1, 'Ground Hit Kinetic Energy of Section 3 for Drogue', 'Drogue Diameter (in)', 'Kinetic Energy (lbf)')

    graph_data2(10, Main, DecentTime, ('12','15','18','24'), 'Decent Time for Different Configurations', 'Main Diameter (in)', 'Time (s)')

    graph_data2(11, Main, Drift0, ('12','15','18','24'), '0 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')

    graph_data2(12, Main, Drift5, ('12','15','18','24'), '5 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')

    graph_data2(13, Main, Drift10, ('12','15','18','24'), '10 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')

    graph_data2(14, Main, Drift15, ('12','15','18','24'), '15 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')

    graph_data2(15, Main, Drift20, ('12','15','18','24'), '20 mi/hr Drift for Different Configurations', 'Main Diameter (in)', 'Drift (ft)')
    
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
