
import numpy as np
import matplotlib.pyplot as plt
from columnar import columnar

class Matboard:
    def __init__(self, thickness, x, y, x2, y2, base, failure_mode):
        '''
        thickness > float
            The shortest side of the matboard

        x, y > floats
            The position of the bottom left corner of the matboard.

        x2, y2 > floats
            The position of the top right corner of the matboard.

        base > float
            The length of the base of the matboard
        
        failure mode
            What failure mode it is

            None: No failure mode needs to be considered
            5: Flange buckling (tips supported)
            7: Web buckling
        '''

        self.thickness = thickness
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.length = np.sqrt((x2-x)**2+(y2-y)**2-thickness**2)
        self.center_of_mass = np.array([
            0.5*(self.x+self.x2),
            0.5*(self.y+self.y2),
        ])
        self.b = base
        self.h = abs(self.y2-self.y)
        self.moi = 1/12 * self.b * self.h**3
        self.area = self.b * self.h

        # print(self.area)
        self.failure_mode = failure_mode

        if self.failure_mode == 5:
            self.factor = 4*np.pi**2/12 * (self.h/self.length)**2
        elif self.failure_mode == 7:
            self.factor = 6*np.pi**2/12 * (self.b/(self.length/2))**2

class Section:
    def __init__(self, start_pos, thickness, span, available_area, matboard_data):
        '''
        star_pos > float
            The starting position of the section

        thickness > float
            The shortest side of the matboard

        span > float
            The total span of the section
        
        available_area > float
            The available area of the matboard that can be used

        matboard_data > 2d list:
        [
            [x1, y1, x2, y2, base, failure mode],
            ...
        ]
            Contains data about each matboard used
        '''
        self.start_pos = start_pos
        self.thickness = thickness
        self.span = span
        self.available_area = available_area

        self.matboard_list = []
        self.glue_list = matboard_data[1]
        self.centroid_thickness = matboard_data[2]

        # Construct a list of matboards used
        for matboard in matboard_data[0]:
            self.matboard_list.append(Matboard(self.thickness, matboard[0], matboard[1], matboard[2], matboard[3], matboard[4], matboard[5]))

        # Calculate location of center of mass of Matboard
        self.center_of_mass = np.sum([matboard.area*matboard.center_of_mass for matboard in self.matboard_list], axis=0)/np.sum([matboard.area for matboard in self.matboard_list])

        self.area = sum([matboard.area for matboard in self.matboard_list])

        # Calculate moment of inertia
        self.moi = 0
        for matboard in self.matboard_list:
            distance = matboard.center_of_mass[1] - self.center_of_mass[1]
            extra_moi = matboard.area * distance**2
            self.moi += matboard.moi + extra_moi

        # Note, this is not the cross sectional area, but the total matboard area used
        length = np.sum([matboard.area/matboard.thickness for matboard in self.matboard_list])
        self.used_area = length * self.span
        self.area_usage = self.used_area/self.available_area*100

        # Calculate Q
        accuracy = 10000
        self.max_y = max([matboard.y + matboard.h for matboard in self.matboard_list])
        self.y_pos = np.linspace(0, self.max_y, accuracy)
        self.Q = np.zeros(accuracy)
        for i in range(len(self.y_pos)):
            for matboard in self.matboard_list:
                if matboard.y >= self.y_pos[i]:
                    self.Q[i] += matboard.area*(matboard.y + matboard.h/2 - self.center_of_mass[1])

                elif matboard.y < self.y_pos[i] and matboard.y + matboard.h >= self.y_pos[i]:
                    difference = matboard.y + matboard.h - self.y_pos[i]
                    new_cm_top = self.y_pos[i] + difference/2
                    area = matboard.b * (matboard.y + matboard.h - self.y_pos[i])
                    self.Q[i] += area*(new_cm_top-self.center_of_mass[1])

        # print(max(self.Q))
        plt.plot(self.Q,self.y_pos)
        # plt.show()

    def print_data(self):
        headers = ['Property', 'Value']

        data = [
            ["Center of mass from bottom (mm)", round(self.center_of_mass[1], 2)],
            ["Moment of inertia (x0^6 mm^4)", round(self.moi/10**6, 2)],
            ["Matboard Used (%)", str(round(self.area_usage, 2))+"%"]
        ]

        table = columnar(data, headers, no_borders=True)
        print(table)

class Bridge:
    def __init__(self, E, span, section_data, loads, support=None):
        '''
        E: float
            > Young's Modulus
        span: float
            > Span of the bridge
        section_data: list
            > contains all the data for all the sections it is composed of
        loads: list
        [
            [x]
        ]
        section_data: list
            > contains all the data for all the sections the support is composed of
            > Default to None
        '''
        # Constants
        self.max_tensile = 30
        self.max_compressive = 6
        self.max_shear = 4
        self.max_glue_shear = 2
        self.poisson = 0.2
        self.E = 4000

        # Data
        self.E = E
        self.span = span
        self.section_data = section_data
        self.loads = loads
        self.section_list = []
        for section in self.section_data:
            self.section_list.append(Section(section[0], section[1], section[2], section[3], section[4]))
        self.support = support
        precision = 1500

        self.x_points = np.linspace(0, self.span, precision)

        # Physical Quantities
        self.height = np.zeros(precision)
        self.com = np.zeros(precision)
        for i in range(precision):
            for section in self.section_list:
                if section.start_pos < self.x_points[i] <= section.start_pos + section.span:
                    self.height[i] = section.max_y 
                    self.com[i] = section.center_of_mass[1]

        # Load Distribution

        self.load_distribution = np.zeros(precision)
        for i in range(precision):
            for load in self.loads:
                if load[0] <= self.x_points[i] <= load[1]:
                    self.load_distribution[i] = load[2]


        # Shear Force
        self.shear_force = np.zeros(precision)
        for i in range(1, precision-1):
            # numerically integrate using midpoint rule
            width = self.x_points[i+1]-self.x_points[i]
            height = self.load_distribution[i-1]

            if i > 0:
                self.shear_force[i] = self.shear_force[i-1] + width*height
            else:
                self.shear_force[i] = width*height

        # Moment
        self.moment = np.zeros(precision)
        for i in range(1, precision-1):
            # numerically integrate using midpoint rule
            width = self.x_points[i+1]-self.x_points[i]
            height = self.shear_force[i-1]

            if i > 0:
                self.moment[i] = self.moment[i-1] + width*height
            else:
                self.moment[i] = width*height
    
        # rigidity
        self.rigidity = np.zeros(precision)
        self.moi = np.zeros(precision)
        for i in range(precision):
            for section in self.section_list:
                if section.start_pos <= self.x_points[i] <= section.start_pos + section.span:
                    self.rigidity[i] = self.E * section.moi
                    self.moi[i] = section.moi

        # Curvature
        self.curvature = self.moment / self.rigidity

        # Slope
        self.slope = np.zeros(precision)
        for i in range(precision):
            # numerically integrate using midpoint rule

            if i < precision-1:
                width = self.x_points[i+1]-self.x_points[i]
                height = 0.5*(self.curvature[i+1]+self.curvature[i])
                self.slope[i] = self.slope[i-1] + width*height

            else:
                self.slope[i] = self.slope[i-1]

        # Displacement
        self.displacement = np.zeros(precision)
        for i in range(precision):
            # numerically integrate using midpoint rule

            if i < precision-1:
                width = self.x_points[i+1]-self.x_points[i]
                height = 0.5*(self.slope[i+1]+self.slope[i])
                self.displacement[i] = self.displacement[i-1] + width*height

            else:
                self.displacement[i] = self.displacement[i-1]
        # Corrections due to constants of integration
        C3 = (0-self.displacement[-1])/self.span
        self.displacement = self.displacement + C3*self.x_points
        self.slope = self.slope + C3
        
        # Middle Support
        if not self.support == None:
            extra_load = 1/30*1000*0.7818

            for i in range(precision):
                if 0 <= self.x_points[i] <= 30:
                    self.load_distribution[i] -= extra_load/2
                if 475 <= self.x_points[i] <= 505:
                    self.load_distribution[i] += extra_load
                if 950 <= self.x_points[i] <= 980:
                    self.load_distribution[i] -= extra_load/2

            # Shear Force
            self.shear_force = np.zeros(precision)
            for i in range(1, precision-1):
                # numerically integrate using midpoint rule
                width = self.x_points[i+1]-self.x_points[i]
                height = self.load_distribution[i-1]

                if i > 0:
                    self.shear_force[i] = self.shear_force[i-1] + width*height
                else:
                    self.shear_force[i] = width*height

            # Moment
            self.moment = np.zeros(precision)
            for i in range(1, precision-1):
                # numerically integrate using midpoint rule
                width = self.x_points[i+1]-self.x_points[i]
                height = self.shear_force[i-1]

                if i > 0:
                    self.moment[i] = self.moment[i-1] + width*height
                else:
                    self.moment[i] = width*height

            '''
            calculations for support
            '''
            self.support = self.support[0]
            self.support_section = Section(self.support[0], self.support[1], self.support[2], self.support[3], self.support[4])


            '''
            Failure Modes
            '''
            self.applied_pressure = extra_load*30/self.support_section.area
            self.global_buckling = (np.pi**2*self.support_section.moi*self.E/(600**2))/self.support_section.area
        
            self.global_buckling_support_fos = self.global_buckling/self.applied_pressure
            self.compressive_support_fos = self.max_compressive/self.applied_pressure

            self.support_flange_buckling = []

            for matboard in self.support_section.matboard_list:
                if matboard.failure_mode == 5:
                    failure = self.E/(1-self.poisson**2) * 4*np.pi**2/12 * (matboard.h/matboard.length)**2
                    self.support_flange_buckling.append(failure)
            
            self.support_flange_buckling_fos = min(self.support_flange_buckling)/self.applied_pressure

        # FAILURE MODES

        # Flexural Failure
        # Tensile Strengths
        self.tensile_failure_list = np.zeros(precision)
        for i in range(precision):
            if self.moment[i] > 0:
                self.tensile_failure_list[i] = abs(self.moment[i]*(self.com[i])/self.moi[i])
            else:
                self.tensile_failure_list[i] = abs(self.moment[i]*(self.height[i]-self.com[i])/self.moi[i])

        self.compressive_failure_list = np.zeros(precision)

        for i in range(precision):
            if self.moment[i] < 0:
                self.compressive_failure_list[i] = abs(self.moment[i]*(self.com[i])/self.moi[i])
            else:
                self.compressive_failure_list[i] = abs(self.moment[i]*(self.height[i]-self.com[i])/self.moi[i])

        # Shear Failure
        self.main_shear_stresses = []
        self.glue_shear_stresses = []

        for section in self.section_list:
            temp_glue_shear_stress = []

            for i in range(len(section.glue_list)):
                index = int(10000 * section.glue_list[i][0] / section.max_y) - 1

                if index < len(section.Q):
                    Q = section.Q[index]
                else:
                    Q = section.Q[-1]
            
                VI = max([self.shear_force[j]/self.moi[j] for j in range(len(self.x_points)) if section.start_pos <= self.x_points[j] <= section.start_pos + section.span])
                b = section.glue_list[i][1]
                temp_glue_shear_stress.append(VI*Q/b)
            self.glue_shear_stresses.append(temp_glue_shear_stress)


            index = int(10000 * section.center_of_mass[1] / section.max_y) - 1
            if index < len(section.Q):
                Q = section.Q[index]
            else:
                Q = section.Q[-1]
            VI = max([self.shear_force[j]/self.moi[j] for j in range(len(self.x_points)) if section.start_pos <= self.x_points[j] <= section.start_pos + section.span])
            b = section.centroid_thickness
            self.main_shear_stresses.append(VI*Q/b)
            # print(Q)
        # Plate Buckling

        # Equation (5): Buckling of compressive flange between the webs
        self.buckling_5_top = [99999999]
        self.buckling_5_bot = [99999999]

        self.buckling_7_top = [99999999]
        self.buckling_7_bot = [99999999]

        for section in self.section_list:
            for matboard in section.matboard_list:
                if matboard.failure_mode == 5:
                    failure = self.E/(1-self.poisson**2) * 4*np.pi**2/12 * (matboard.h/matboard.length)**2
                    self.buckling_5_top.append(failure)

                if matboard.failure_mode == 5.1:
                    failure = self.E/(1-self.poisson**2) * 4*np.pi**2/12 * (matboard.h/matboard.length)**2
                    self.buckling_5_bot.append(failure)

                if matboard.failure_mode == 6:
                    failure = self.E/(1-self.poisson**2) * 0.425*np.pi**2/12 * (matboard.h/matboard.length)**2
                    self.buckling_6.append(failure)

                if matboard.failure_mode == 7:
                    conversion = matboard.length/matboard.h

                    height_top = section.max_y-section.center_of_mass[1] * conversion
                    height_bot = section.center_of_mass[1] * conversion

                    failure_top = self.E/(1-self.poisson**2) * 6*np.pi**2/12 * (matboard.thickness/(height_top))**2
                    self.buckling_7_top.append(failure_top)

                    failure_bot = self.E/(1-self.poisson**2) * 6*np.pi**2/12 * (matboard.thickness/(height_bot))**2
                    self.buckling_7_bot.append(failure_bot)

        self.tensile_fos = self.max_tensile/max(self.tensile_failure_list)
        self.compressive_fos = self.max_compressive/max(self.compressive_failure_list)
        self.wall_shear_fos = self.max_shear/max(self.main_shear_stresses)
        # self.compressive_flange_fos = min(self.buckling_5)/max(self.compressive_failure_list)

        # COMPRESSIVE FLANGE BUCKLING
        self.compressive_flange_fos_1 = min([min(self.buckling_5_top)/self.compressive_failure_list[i] for i in range(len(self.x_points)) if self.moment[i] > 0])
        if max(self.moment) < 0:
            self.compressive_flange_fos_2 = min([min(self.buckling_5_bot)/self.compressive_failure_list[i] for i in range(len(self.x_points)) if self.moment[i] < 0])
        else:
            self.compressive_flange_fos_2 = 9999999
        self.compressive_flange_fos = min([self.compressive_flange_fos_1, self.compressive_flange_fos_2])

        # WEB BUCKLING
        self.web_buckling_fos_1 = min([min(self.buckling_7_top)/self.compressive_failure_list[i] for i in range(len(self.x_points)) if self.moment[i] > 0])
        if max(self.moment) < 0:
            self.web_buckling_fos_2 = min([min(self.buckling_7_bot)/self.compressive_failure_list[i] for i in range(len(self.x_points)) if self.moment[i] < 0])
        else:
            self.web_buckling_fos_2 = 9999999

        self.web_buckling_fos = min([self.web_buckling_fos_1, self.web_buckling_fos_2])

        if self.support == None:
            self.fos_list = [self.tensile_fos, self.compressive_fos, self.wall_shear_fos, self.compressive_flange_fos, self.web_buckling_fos]
            self.total_percent = sum([section.area_usage for section in self.section_list])

        else:
            self.fos_list = [self.tensile_fos, self.compressive_fos, self.wall_shear_fos, self.compressive_flange_fos, self.web_buckling_fos, self.global_buckling_support_fos, self.support_flange_buckling_fos, self.compressive_support_fos]
            self.total_percent = sum([section.area_usage for section in self.section_list]) + self.support_section.area_usage

        self.area_usage = self.total_percent
    '''
            if self.failure_mode == 5:
                self.factor = 4*np.pi**2/12 * (self.h/self.length)**2
            elif self.failure_mode == 7:
                self.factor = 6*np.pi**2/12 * (self.b/(self.length/2))**2
    '''
    def print_data(self):
        
        for i in range(len(self.section_list)):
            print( "=========================================================================")
            print(f"============================ SECTION {i+1} ==================================")
            print( "=========================================================================")

            headers = ['Property', 'Value']
            data = [
                ["Center of mass from bottom (mm)", round(self.section_list[i].center_of_mass[1], 2)],
                ["Moment of inertia (x0^6 mm^4)", round(self.section_list[i].moi/10**6, 2)],
                ["Matboard Used (%)", str(round(self.area_usage, 2))+"%"],
            ]

            table = columnar(data, headers, no_borders=True)
            print(table)

        print( "=========================================================================")
        print(f"=========================== BRIDGE DATA =================================")
        print( "=========================================================================")
        headers = ['Failure Mode', 'Value']
        data = [
            ["Tensile Failure FOS", str(round(self.max_tensile/max(self.tensile_failure_list), 2))],
            ["Compressive Failure FOS", str(round(self.max_compressive/max(self.compressive_failure_list), 2))],
            ["Wall Shear Failure FOS", str(round(self.max_shear/max(self.main_shear_stresses), 2))],
            ["Glue Shear Failure FOS", str(round(self.max_glue_shear/np.amax(self.glue_shear_stresses), 2))],
            ["Compressive Flange Buckling FOS", str(round(self.compressive_flange_fos, 2))],
            ["Web Buckling FOS", str(round(self.web_buckling_fos, 2))],
        ]
        table = columnar(data, headers, no_borders=True)
        print(table)

        if not self.support == None:
            print( "=========================================================================")
            print(f"=========================== SUPPORT DATA ================================")
            print( "=========================================================================")
            headers = ['Failure Mode', 'Value']
            data = [
                ["Compressive Failure FOS", str(round(self.compressive_support_fos, 2))],
                ["Global Buckling FOS", str(round(self.global_buckling_support_fos, 2))],
                ["Flange Buckling FOS", str(round(self.support_flange_buckling_fos, 2))],
            ]
            table = columnar(data, headers, no_borders=True)
            print(table)

    def plot_shear(self):
        plt.figure()
        plt.plot(self.x_points, self.shear_force)
        plt.title("Shear Force Diagram")
        plt.ylabel("Shear Force (N)")
        plt.xlabel("Location (mm)")
        plt.show()

    def plot_moment(self):
        plt.figure()
        plt.gca().invert_yaxis()
        plt.plot(self.x_points, self.moment)
        plt.title("Moment Diagram")
        plt.ylabel("Moment (N mm)")
        plt.xlabel("Location (mm)")
        plt.show()

    def plot_curvature(self):
        plt.figure()
        plt.gca().invert_yaxis()
        plt.plot(self.x_points, self.curvature)
        plt.title("Curvature Diagram")
        plt.ylabel("Curvature (1/mm)")
        plt.xlabel("Location (mm)")
        plt.show()

    def plot_deflection(self):
        plt.figure()
        plt.plot(self.x_points, self.displacement)
        plt.title("Actual Shape")
        plt.ylabel("Deflection (mm)")
        plt.xlabel("Location (mm)")
        plt.show()

    def plot_smc(self):
        plt.figure(figsize=(5,12))
        plt.subplot(5,1,1)
        plt.tight_layout(pad=3.0)
        plt.plot(self.x_points, self.load_distribution)
        plt.title("Load Distribution Diagram")
        plt.ylabel("Load (N/mm)")
        plt.xlabel("Location (mm)")

        plt.subplot(5,1,2)
        plt.tight_layout(pad=3.0)
        plt.plot(self.x_points, self.shear_force)
        plt.title("Shear Force Diagram")
        plt.ylabel("Shear Force (N)")
        plt.xlabel("Location (mm)")

        plt.subplot(5,1,3)
        plt.gca().invert_yaxis()
        plt.plot(self.x_points, self.moment)
        plt.title("Moment Diagram")
        plt.ylabel("Moment (N mm)")
        plt.xlabel("Location (mm)")

        plt.subplot(5,1,4)
        plt.gca().invert_yaxis()
        plt.plot(self.x_points, self.curvature)
        plt.title("Curvature Diagram")
        plt.ylabel("Shear Force (1/mm)")
        plt.xlabel("Location (mm)")

        plt.subplot(5,1,5)
        plt.plot(self.x_points, self.displacement)
        plt.title("Actual Shape")
        plt.ylabel("Deflection (mm)")
        plt.xlabel("Location (mm)")

        plt.show()

from Classes import *

'''
Project Specifications
'''
matboard_area = 813*1016
matboard_thickness = 1.27
matboard_mass = 0.750
bridge_span = 980
P = 1000 # Newtons
E = 4000 # MPa


max_tensile = 30
max_compressive = 6
max_shear = 4

'''
Bridge Designs
'''

def design_b_generator(a, b, c, h, t):
    angle = np.arctan(2*h/(b-a))
    base_length = t/np.sin(angle)
    # Coordinate of the bottom left corner of the right diagonal web
    coord = (
        (b-a)/2+a-t*np.sin(angle),
        a+t*np.cos(angle)
    )
    beam_information = [
        [(b-a)/2,                   0,      (b-a)/2 + a,             t      , a             , None], # Bottom Flange
        [0,                         t+h,    b,                       3*t+h  , b             , 5], # Top Flange
        # [0,                         t+h+t,  b,                       2*t+h+t, b], # Top Flange
        [0,                         t,      (b-a)/2 + base_length,   t+h    , base_length   , 7], # Left Diagonal Web
        [(b-a)/2 + a - base_length, t,      b,                       t+h    , base_length  , 7], # Left Diagonal Web
        # [base_length,                         t+h,    base_length+t,                     h      , t             , None], # Glue Tab 1
        # [b-base_length,                       t+h,    b-base_length-t,                   h  , t             , None], # Glue Tab 2
        # [base_length,                         t,      base_length+t,                     t+t      , t             , None], # Glue Tab 1
        # [a-base_length,                       t,    a-base_length-t,                     t+t  , t             , None], # Glue Tab 2
    ]

    glue_information = [
        [t,           8],
        [t+h,         12]
    ]
    return (beam_information, glue_information, 2*t/np.sin(angle))

def design_c_generator(a, b, t):
    beam_information = [
        [0,0,a,t,   a,   5], # Bottom Flange
        [0,b+t,a,b+3*t ,a, 5],
        [0,t,t,b+t,  t, 7],
        [a-t,t,a,b+t,t,7]
    ]

    glue_information = [
        [t,           6],
        [a-t,         6]
    ]

    return (beam_information, glue_information, 2*t)

def design_c_generator_support(a,b, t):
    beam_information = [
        [0,0,a,t,   a,   5], # Bottom Flange
        [0,b+t,a,b+2*t ,a, 5],
        [0,t,t,b+t,  t, 7],
        [a-t,t,a,b+t,t,7]
    ]

    glue_information = [
        [t,           2*t],
        [a-t,         2*t]
    ]

    return (beam_information, glue_information, 2*t)
'''
Calculations
'''

self_weight = 8e-3
reaction_force = (P)/2 + 0.123*30

bridge_loads = [
    (0, 30, reaction_force/30),
    (30, 280, -self_weight),
    (280, 310, -P/60 - self_weight),
    (310, 670, -self_weight),
    (670, 700, -P/60 - self_weight),
    (700, 950, - self_weight),
    (950, 980, reaction_force/30),
]

def optimize_configuration_b():
    '''
    NOTE: THE RANGE FOR THE CONFIGURATIONS ARE MANUALLY ALTERED TO LOOK AT A SPECIFIC RANGE.
    '''
    fos = 0
    configuration = [0,0,0,0]
    for a in np.arange(34, 42, 4):
        for b in np.arange(102, 106, 1):
                c = 0
            # for c in np.arange(0, 20, 5): 
                for h in np.arange(185, 195, 2):
                    print(a,b,c,h)
                    bridge_design = [
                                        [0, matboard_thickness, bridge_span, matboard_area, design_b_generator(a, b, c, h, matboard_thickness)]
                                    ]
                    bridge = Bridge(E, bridge_span, bridge_design, bridge_loads)
                    if bridge.total_percent < 75:
                        if min(bridge.fos_list) > fos:
                            fos = min(bridge.fos_list)
                            configuration = [a,b,c,h]

    print(configuration)

def optimize_configuration_c():
    '''
    NOTE: THE RANGE FOR THE CONFIGURATIONS ARE MANUALLY ALTERED TO LOOK AT A SPECIFIC RANGE.
    '''
    fos = 0
    configuration = [0,0,0,0]
    a = 100
    for b in np.arange(113, 116, 1):
        for c in np.arange(60,63,1):
                print(a,b,c)
                bridge_design = [
                                    [0, matboard_thickness, bridge_span, matboard_area, design_c_generator(a, b, matboard_thickness)]
                                ]
                support_design = [
                                    [0, matboard_thickness, 600, matboard_area, design_c_generator_support(c, matboard_thickness)]
                                ]
                bridge = Bridge(E, bridge_span, bridge_design, bridge_loads, support_design)
                if bridge.total_percent < 80:
                    if min(bridge.fos_list) > fos:
                        fos = min(bridge.fos_list)
                        configuration = [a,b,c]

    print(configuration)

# bridge_design = [
#                     [0, matboard_thickness, bridge_span, matboard_area, design_c_generator(100, 114, matboard_thickness)]
#                 ]
# support_design = [
#                     [0, matboard_thickness, 600, matboard_area, design_c_generator_support(50, 80, matboard_thickness)]
#                 ]
# bridge = Bridge(E, bridge_span, bridge_design, bridge_loads, support_design)
# bridge.print_data()
# bridge.plot_smc()