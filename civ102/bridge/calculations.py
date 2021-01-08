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

bridge_design = [
                    [0, matboard_thickness, bridge_span, matboard_area, design_c_generator(100, 114, matboard_thickness)]
                ]
support_design = [
                    [0, matboard_thickness, 600, matboard_area, design_c_generator_support(50, 80, matboard_thickness)]
                ]
bridge = Bridge(E, bridge_span, bridge_design, bridge_loads, support_design)
bridge.print_data()
bridge.plot_smc()