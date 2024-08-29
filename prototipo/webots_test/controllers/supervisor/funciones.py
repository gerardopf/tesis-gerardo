""" =========================================================================
# FUNCTIONS TO MEASURE METRICS AND GENERATE GRAPHS
# =========================================================================
# Autor: José Alejandro Rodríguez Porras
# ========================================================================= """

import numpy as np
import math

def FormationError(FAct, FDes, NStart, N):
# Calculates the mse error between the current formation and the desired one
# Parameters:
#   FAct = Adjacency matrix of the current formation
#   FDes = Adjacency matrix of the target (desired) formation
# Output:
#   error = Mean squared error of the current formation compared to the desired
# one
    s1 = len(FAct[0])
    suma = 0
    for i in range(NStart,N):
        for j in range(NStart,N):
            mDif = (FAct[i][j] - FDes[i][j])**2 # Squared difference
            suma = suma + mDif		   # columns and rows sum
    tot = (NStart-N)**2		   # Agent quantity
    error = suma/tot			   # mean error
    return error


def DistBetweenAgents(X,NStart,N):
# Generates the matrix with the distance between the agents.
# Parameters:
#   X = Matrix with the current position of the agents vectors (x,y)
# Output:
#   mDist = Adjacency matrix of the graph produced by the current position
# of the agents

    n = N-NStart		# Agent quantity
    mDist = np.zeros([N,N])	# Matrix initialization

    for i in range(NStart,N):
        for j in range(NStart,N):
            dij1 = X[0,i] - X[0,j]
            dij2 = X[1,i] - X[1,j]
            normdij = math.sqrt(dij1**2 + dij2**2)    # distance between i & j agents
            mDist[i,j] = normdij		         # distance added to the matrix
    return mDist

def table_gen(real_file, virtual_file):
# Generates the table comparing the physical run with the simulation run

    def format_number(number,symbol = ""):
    # formats the number
        if number == None:
            return " - "
        else:
            return f'{round(number,2):.2f}{symbol}'
            
    import re
    from prettytable import PrettyTable
    # Define a regular expression pattern to match either "_h_" or "_f_"
    
    # loads the file
    initial_conditions_file = real_file
    initial_data = np.load(initial_conditions_file)
    real_begin_alg_time = initial_data['begin_alg_time']
    
    
    data = np.load(virtual_file)
    
    # loads the relevant variables to compare
    fisico = data['fisico']
    r_f = data['r_f']
    l_f = data['l_f']
    a_f = data['a_f']
    trajectory_data = data['trajectory_data']
    rot_data = data['rot_data']
    velocity_data = data['velocity_data']
    normV_data = data['normV_data']
    formation_mse_data = data['formation_mse_data']
    obj_data = data['obj_data']
    obs_data = data['obs_data']
    total_cycle = data['total_cycle']
    form_cycle = data['form_cycle']
    obj_cycle = data['obj_cycle']
    quantO = data['quantO']
    posObsAct = data['posObsAct']
    sizeO = data['sizeO']
    NStart = data['NStart']
    N = data['N']
    pObjVec = data['pObjVec']
    begin_alg_time = data['begin_alg_time']
    fisico = data['fisico']
    r_initial_conditions = data['r_initial_conditions']
    r_obs = data['r_obs']
    r_obj = data['r_obj']
    TIME_STEP = data['TIME_STEP']
    agent_setup = data['agent_setup']
    obs_active = data['obs_active']
    initial_pos_setup = data['initial_pos_setup']
    r = data['r']
    R = data['R']
    MAX_SPEED = data['MAX_SPEED']
    form_shape = data['form_shape']
    rigidity_level = data['rigidity_level']
    total_agent_number = data['total_agent_number']
    NMax = data['NMax']
    obj_marker = data['obj_marker']
    obs_start_marker = data['obs_start_marker']
    setup_starting_point = data['setup_starting_point']
    formation_edge = data['formation_edge']
    
    # using regex it looks for the h or f letter of the file (representing hybrid (h) or physical (f))
    pattern = re.compile(r'(_[hf]_)')
    filename_without_extension = initial_conditions_file.split('.')[0]
    # extracts the code representing the scenario
    pattern_code = re.compile(r'A_([^_]+)_')
    # extracts the number of trial 
    pattern_code_number = re.compile(r'_([^_]+)$')
    # Use re.sub to replace the matched pattern with '_t_' meaning table
    table_namefile = re.sub(pattern, '_t_', filename_without_extension)
    match = re.search(pattern_code, filename_without_extension)
    if match:
        extracted_scenario = match.group(1)
    
        
    match_number = re.search(pattern_code_number, filename_without_extension)
    if match_number:
        extracted_trial_number = match_number.group(1)
    
    real_time_compensation = 1.45 # it is a constant to make up for the compensation
    # for the physical run time step, since because of the delay caused by the 
    # comms exchange between the computer, server and agents each time step of the 
    # physical run is about 1.45 times the simulation one
    
    # the comp in this variables indicates the comparison data, being the physical
    # run one
    
    # physical run 
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    normV_data_comp = initial_data['normV_data']
    formation_mse_data_comp = initial_data['formation_mse_data']
    total_cycle_comp = initial_data['total_cycle']
    obj_cycle_comp = initial_data['obj_cycle']
    TIME_STEP_comp = initial_data['TIME_STEP']*real_time_compensation
    
    # the real also indicates it is a variable from the physical run used for comparison
    real_total_cycle = total_cycle_comp
    real_trajectory_data = initial_data['trajectory_data']
    real_x_positions = real_trajectory_data[:, 0, :]
    real_y_positions = real_trajectory_data[:, 1, :]
    real_pObjVec = initial_data['pObjVec']
    real_x_pObjVec = real_pObjVec[0]
    real_y_pObjVec = real_pObjVec[1]
    real_NStart = NStart - 1 
    real_cm_success = None
    real_leader_success = None
    #when the leader reaches 0.5 m it is considered a leader success
    leader_success_threshold = 0.5 
    #when the center of mass of the formation reaches the leader success threshold plus the 
    #center of mass of the formation distance, it is considered a formation success
    cm_success_threshold = leader_success_threshold + math.sqrt(3)*formation_edge*3/6
    #print(cm_success_threshold)
    # scans the run to find out if and when the leader was successful to reach the objective
    for coordinate_success, coordinate_value in enumerate(real_x_positions[obj_cycle_comp:real_total_cycle], start = obj_cycle_comp):
        #print(real_x_positions[coordinate_success, NStart])
        if (abs(real_x_positions[coordinate_success, real_NStart]-real_x_pObjVec)<leader_success_threshold and abs(real_y_positions[coordinate_success, real_NStart]-real_y_pObjVec)<leader_success_threshold):
            real_leader_success = (coordinate_success-real_begin_alg_time)
            #print(real_leader_success)
            #print("******************************************************************************")
            break      
        #coordinate_success = coordinate_success+1
    
    #coordinate_success = obj_cycle_comp
    # scans the run to find out if and when the formation was successful to reach the objective    
    for coordinate_success, coordinate_value in enumerate(real_x_positions[obj_cycle_comp:real_total_cycle], start = obj_cycle_comp):
        #print(real_x_positions[coordinate_success, NStart])
        #print(real_total_cycle)
        if (abs(np.mean(real_x_positions[coordinate_success, real_NStart:N])-real_x_pObjVec)<cm_success_threshold and abs(np.mean(real_y_positions[coordinate_success, real_NStart:N])-real_y_pObjVec)<cm_success_threshold):
            real_cm_success = (coordinate_success-real_begin_alg_time)
            print(real_cm_success)
            #print("******************************************************************************")
            break
          
        #coordinate_success = coordinate_success+1
    #------------------------------------------------------------------------------------------------------------------------------------------------------     
    # simulation run 
    #------------------------------------------------------------------------------------------------------------------------------------------------------    
    x_positions = trajectory_data[:, 0, :]
    y_positions = trajectory_data[:, 1, :]
    x_pObjVec = pObjVec[0]
    y_pObjVec = pObjVec[1]
    cm_success = None
    leader_success = None
    #here
    #acoordinate_success = obj_cycle
    for coordinate_success, coordinate_value in enumerate(x_positions[obj_cycle:total_cycle],start = obj_cycle):
        #print(real_x_positions[coordinate_success, NStart])
        if (abs(x_positions[coordinate_success, real_NStart]-x_pObjVec)<leader_success_threshold and abs(y_positions[coordinate_success, real_NStart]-y_pObjVec)<leader_success_threshold):
            leader_success = (coordinate_success-begin_alg_time)
            #print(leader_success*TIME_STEP/1000)
            #print("******************************************************************************")
            break      
        #coordinate_success = coordinate_success+1
        #print(coordinate_success)
    
    #coordinate_success = obj_cycle_comp    
    for coordinate_success, coordinate_value in enumerate(x_positions[obj_cycle:total_cycle], start = obj_cycle):
        #print(real_x_positions[coordinate_success, NStart])
        if (abs(np.mean(x_positions[coordinate_success, real_NStart:N])-x_pObjVec)<cm_success_threshold and abs(np.mean(y_positions[coordinate_success, real_NStart:N])-y_pObjVec)<cm_success_threshold):
            cm_success = (coordinate_success-begin_alg_time)
            print(cm_success*TIME_STEP/1000)
            #print("******************************************************************************")
            break 
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    # Create a PrettyTable object
    table = PrettyTable()
    
    # Define the table columns
    table_columns = ["Métrica", "Físico", "Simulado", r'$\Delta$', "Dif. Relativa"]
    
    
    for title_index,table_title in enumerate(table_columns):
        table_columns[title_index] = r'\textbf{'+table_title+"}"
        
        
        
    table.field_names = table_columns
    
    # calculate the metrics (mean,delta,relative error) of the relevant parameters of the run
    normV_comp_mean = round(np.mean(normV_data_comp[obj_cycle_comp:total_cycle_comp]), 2)
    normV_mean = round(np.mean(normV_data[obj_cycle:total_cycle]), 2)
    formation_mse_comp_mean = round(np.mean(formation_mse_data_comp[obj_cycle_comp:total_cycle_comp]), 2)
    formation_mse_mean = round(np.mean(formation_mse_data[obj_cycle:total_cycle]), 2)
    
    normV_delta = normV_comp_mean-normV_mean
    formation_mse_delta = formation_mse_comp_mean-formation_mse_mean
    
    normV_error = abs(normV_delta)*100/(max(normV_comp_mean,normV_mean))
    formation_mse_error = abs(formation_mse_delta)*100/(max(formation_mse_comp_mean,formation_mse_mean))
    print(formation_mse_error)
    # Add data to the table
    table.add_row(["Promedio norma de velocidades (m/s)", f'{normV_comp_mean:.2f}', f'{normV_mean:.2f}',format_number(normV_delta,""), format_number(normV_error,"\%")])
    table.add_row(["Promedio del mse de la formación", f'{formation_mse_comp_mean:.2f}', f'{formation_mse_mean:.2f}',format_number(formation_mse_delta,""), format_number(formation_mse_error,"\%")])
    
    # calculate the metrics (mean,delta,relative error) of the relevant parameters of the run
    total_cycle_comp = round((initial_data['total_cycle']-initial_data['begin_alg_time'])*TIME_STEP_comp/1000, 2)
    form_cycle_comp = round((initial_data['form_cycle']-initial_data['begin_alg_time'])*TIME_STEP_comp/1000, 2)
    obj_cycle_comp = round((initial_data['obj_cycle']-initial_data['begin_alg_time'])*TIME_STEP_comp/1000, 2)
    try:
        real_leader_success_comp = round(real_leader_success*TIME_STEP_comp/1000, 2)
    except:
        real_leader_success_comp = None
    try:
        real_cm_success_comp = round(real_cm_success*TIME_STEP_comp/1000, 2)
    except:
        real_cm_success_comp = None
    try:
        real_success_diff_comp = abs(real_cm_success_comp-real_leader_success_comp)
    except:
        real_success_diff_comp = None
    total_cycle_table = round(total_cycle*TIME_STEP/1000, 2)
    form_cycle_table = round((form_cycle+1)*TIME_STEP/1000, 2)
    obj_cycle_table = round(obj_cycle*TIME_STEP/1000, 2)
    try:
        leader_success_table = round(leader_success*TIME_STEP/1000, 2)
    except:
        leader_success_table = None
    try:
        cm_success_table = round(cm_success*TIME_STEP/1000, 2)
    except:
        cm_success_table = None
    
    try:
        success_diff_table = abs(cm_success_table-leader_success_table)
    except:
        success_diff_table = None
    print(success_diff_table)
    
    total_cycle_delta = total_cycle_comp-total_cycle_table
    form_cycle_delta = form_cycle_comp-form_cycle_table
    obj_cycle_delta = obj_cycle_comp-obj_cycle_table
    try:
        leader_success_delta = real_leader_success_comp-leader_success_table
    except:
        leader_success_delta = None
    try:
        cm_success_delta = real_cm_success_comp-cm_success_table
    except:
        cm_success_delta = None
    try:
        success_diff_delta = real_success_diff_comp-success_diff_table
    except:
        success_diff_delta = None
    
    total_cycle_error = abs(total_cycle_delta)*100/(max(total_cycle_comp,total_cycle_table))
    form_cycle_error = abs(form_cycle_delta)*100/(max(form_cycle_comp,form_cycle_table))
    obj_cycle_error = abs(obj_cycle_delta)*100/(max(obj_cycle_comp,obj_cycle_table))
    
    try:
        leader_success_error = abs(leader_success_delta)*100/(max(real_leader_success_comp,leader_success_table))
    except:
        leader_success_error = None
    
    try:
        cm_success_error = abs(cm_success_delta)*100/(max(real_cm_success_comp,cm_success_table))
    except:
        cm_success_error = None
    try:
        success_diff_error = abs(success_diff_delta)*100/(max(real_success_diff_comp,success_diff_table))
    except:
        success_diff_error = None
    table.add_row(["Duración total de la corrida (s)", format_number(total_cycle_comp,""), format_number(total_cycle_table,""),format_number(total_cycle_delta,""), format_number(total_cycle_error,"\%")])
    table.add_row(["\emph{Timestamp} inicio formación (s)", format_number(form_cycle_comp,""), format_number(form_cycle_table,""),format_number(form_cycle_delta,""), format_number(form_cycle_error,"\%")])
    table.add_row(["\emph{Timestamp} inicio seguimiento obj (s)", format_number(obj_cycle_comp,""), format_number(obj_cycle_table,""),format_number(obj_cycle_delta,""), format_number(obj_cycle_error,"\%")])
    table.add_row(["\emph{Timestamp} llegada líder (s)", format_number(real_leader_success_comp,""), format_number(leader_success_table,""),format_number(leader_success_delta,""), format_number(leader_success_error,"\%")])
    table.add_row(["\emph{Timestamp} llegada formación (s)", format_number(real_cm_success_comp,""), format_number(cm_success_table,""),format_number(cm_success_delta,""), format_number(cm_success_error,"\%")])
    table.add_row(["dif. llegada líder y formación (s)", format_number(real_success_diff_comp,""), format_number(success_diff_table,""),format_number(success_diff_delta,""), format_number(success_diff_error,"\%")])
    # Get the LaTeX code for the table
    latex_code = table.get_latex_string()
    # Determine the number of rows and columns
    num_rows = len(table._rows)
    num_columns = len(table_columns)
    
    # Generate the LaTeX code with a full grid
    latex_code_with_full_grid = "\\begin{table}[]\n\centering\n\\begin{tabular}{|" + "|".join(["c"] * num_columns) + "|}\n\\hline\n" + latex_code.replace("\\begin{tabular}", "").replace("\\end{tabular}", "").replace("&", " & ").replace("\\\\", " \\\\ \\hline\n").replace("{" + f'{"c"*num_columns}'+"}", "") + "\\end{tabular}\n\\caption{Comparación de métricas entre corridas en simulación y físico, escenario " + f'{extracted_scenario}, ' + "corrida " + f'{extracted_trial_number},' + f' con {N-real_NStart} agentes' + ".}\n\\label{tabla:" + f'{table_namefile}' + "}\n\\end{table}"
    #latex_code_with_full_grid = ("\\begin{table}[]\n\\begin{tabular}{|" + "|".join(["c"] * num_columns) + "|}\n\\hline\n"+ latex_code.replace("\\begin{tabular}", "").replace("\\end{tabular}", "").replace("&", " & ").replace("\\\\", " \\\\ \\hline\n") +"\\end{tabular}\n\caption{Comparación de métricas entre corridas en simulación y físico, escenario "+f'{extracted_scenario}, '+"corrida "+f'{extracted_trial_number}'+".}\n\label{tabla:"+f'{table_namefile}'+"}\n\end{table}")
    
    import pandas as pd
    from openpyxl import load_workbook
    import os
    from openpyxl import Workbook
    
    # Convert the PrettyTable to a pandas DataFrame
    data = [table.field_names] + table._rows
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Convert all columns except 'Dif. Relativa' to numeric
    df = df.map(lambda x: x.replace(' - ', '') if isinstance(x, str) else x)
    df = df.apply(lambda x: pd.to_numeric(x, errors='ignore') if x.name != r'\textbf{Dif. Relativa}' else x)
    
    # Convert 'Dif. Relativa' column to percentages
    df[r'\textbf{Dif. Relativa}'] = df[r'\textbf{Dif. Relativa}'].map(lambda x: x.replace('\\', '') if isinstance(x, str) else x)
    df[r'\textbf{Dif. Relativa}'] = pd.to_numeric(df[r'\textbf{Dif. Relativa}'], errors='ignore')
    #df[r'\textbf{Dif. Relativa}'] = pd.to_numeric(df[r'\textbf{Dif. Relativa}'], errors='coerce')  # Convert to numeric, treating errors as NaN
    #df[r'\textbf{Dif. Relativa}'] = df[r'\textbf{Dif. Relativa}'] / 100  # Assuming the values are in percentage format
    #df[r'\textbf{Dif. Relativa}'] = df[r'\textbf{Dif. Relativa}'].apply(lambda x: f'{x:.2%}' if not pd.isna(x) else x)
    # Load the existing Excel file
    existing_file_path = 'finaltrials_tables.xlsx'
    if not os.path.exists(existing_file_path):
        # If it doesn't exist, create it
        workbook = Workbook()
        workbook.save(existing_file_path)
    sheet_to_search = f'{extracted_scenario}'
    # checks if the scenario sheet in the excel exists and writes the table on a row selected according to the number of the trial times 10
    # if it doesnt exists it is created
    try:
        whole_existing_df = pd.read_excel(existing_file_path, sheet_name= None)
        existing_df = pd.read_excel(existing_file_path, sheet_name=f'{extracted_scenario}')
        
        # Step 2: Combine new data with existing data
        combined_df = pd.concat([existing_df, df], ignore_index=True)
            
        # Save the updated DataFrame back to the Excel file
        with pd.ExcelWriter(existing_file_path, engine='openpyxl', mode='w') as writer:
            for sheet_name, sheet_df in whole_existing_df.items():
                sheet_df.to_excel(writer, index=False, sheet_name=sheet_name)
            #whole_existing_df.to_excel(writer, index=False)   
            #existing_df.to_excel(writer, index=False, sheet_name= f'{extracted_scenario}', startrow=0)   
            df.to_excel(writer, index=False, sheet_name= f'{extracted_scenario}', startrow=(0+10*(int(f'{extracted_trial_number}')-1))) 
    
    except:
        with pd.ExcelWriter(existing_file_path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, index=False, sheet_name= f'{extracted_scenario}', startrow=(0+10*(int(f'{extracted_trial_number}')-1)))   
            #df.to_excel(writer, index=False, sheet_name= f'{extracted_scenario}', startrow=(0+10*(int(f'{extracted_trial_number}')-1))) 
                
    # Print the LaTeX code with a full grid
    with open(f'finaltrials/{filename_without_extension}/latex.txt', 'a') as file:
            # Use the print function to append new content to the file
            print(latex_code_with_full_grid, file = file)
    
    print(latex_code_with_full_grid)
    
    #print(real_cm_success*TIME_STEP_comp/1000)
    #print(real_leader_success*TIME_STEP_comp/1000)


def figure_gen(file, show_images = 1):
    # generates all the figures related to the run, the animation, creates the folder and file of each run
    # and the latex code with automated captions and naming conventions to put on a latex document.
    # Outputs:
    # - folder containing the file name of the trial and scenario, run
    # - latex.txt that contains the latex code to put the figures with caption and all
    # animation gif of the whole trial
    # for each figure it saves each one in both eps and png format
    # - cm figure showing the trajectory of the center of mass of the formation
    # - mse figure showing the formation mse error through the trial
    # - normV figure showing the velocities norm of the agents through the trial
    # - phiL figure showing the radial velocity of the left wheel of every agent through the trial
    # - phiR figure showing the radial velocity of the right wheel of every agent through the trial
    # - traj figure showing the trajectory of every agent through the trial
    # - xvel figure showing the velocity in x of every agent through the trial
    # - yvel figure showing the velocity in y of every agent through the trial
    # - vel figure showing the velocity´s magnitude of every agent through the trial
    
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import os
    import re
    
    archivo = file
    
    data = np.load(archivo)
    # Extracting the filename without extension from 'archivo'
    filename_without_extension = archivo.split('.')[0]
    # Define the folder name
    main_folder = 'finaltrials'
    folder_name = f'{filename_without_extension}'
    # Create the main folder if it doesn't exist
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    
    # Define the trial folder name
    trial_folder = os.path.join(main_folder, folder_name)
    
    # Create the trial folder inside the main folder
    if not os.path.exists(trial_folder):
        os.makedirs(trial_folder)
    
    
    pattern = r'A_([^_]+)_' # extracts the scenario code
    pattern_number = r'_([^_]+)$' # extracts the trial number
    
    match = re.search(pattern, archivo)
    if match:
        extracted_value = match.group(1)
        print(extracted_value)
    
    match_number = re.search(pattern_number, filename_without_extension)
    if match_number:
        extracted_number = match_number.group(1)
        print(extracted_number)

    with open(f'finaltrials/{filename_without_extension}/latex.txt', 'w') as file:
        pass
    
    def print_latex_figure(filename, caption, label, width):
        latex_code = f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""
    
        # Open a text file in append mode ('a')
        with open(f'finaltrials/{filename_without_extension}/latex.txt', 'a') as file:
            # Use the print function to append new content to the file
            print(latex_code, file = file)
        print(latex_code)
    
        
    
    
    def print_latex_figure_two(filename1,filename2, caption, label, width):
        latex_code = f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename1}}}
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename2}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""
        # Open a text file in append mode ('a')
        with open(f'finaltrials/{filename_without_extension}/latex.txt', 'a') as file:
            # Use the print function to append new content to the file
            print(latex_code, file = file)
        print(latex_code)
    
    #print(data)
    
    #to find out the files within the .npz
    """
    data = np.load('trial.npz', allow_pickle=True)
    print(data.files)
    """
    # loads the relevant variables from the trial
    fisico = data['fisico']
    r_f = data['r_f']
    l_f = data['l_f']
    a_f = data['a_f']
    trajectory_data = data['trajectory_data']
    rot_data = data['rot_data']
    velocity_data = data['velocity_data']
    normV_data = data['normV_data']
    formation_mse_data = data['formation_mse_data']
    obj_data = data['obj_data']
    obs_data = data['obs_data']
    total_cycle = data['total_cycle']
    form_cycle = data['form_cycle']
    obj_cycle = data['obj_cycle']
    quantO = data['quantO']
    posObsAct = data['posObsAct']
    sizeO = data['sizeO']
    NStart = data['NStart']
    N = data['N']
    pObjVec = data['pObjVec']
    begin_alg_time = data['begin_alg_time']
    fisico = data['fisico']
    r_initial_conditions = data['r_initial_conditions']
    r_obs = data['r_obs']
    r_obj = data['r_obj']
    TIME_STEP = data['TIME_STEP']
    agent_setup = data['agent_setup']
    obs_active = data['obs_active']
    initial_pos_setup = data['initial_pos_setup']
    r = data['r']
    R = data['R']
    MAX_SPEED = data['MAX_SPEED']
    form_shape = data['form_shape']
    rigidity_level = data['rigidity_level']
    total_agent_number = data['total_agent_number']
    NMax = data['NMax']
    obj_marker = data['obj_marker']
    obs_start_marker = data['obs_start_marker']
    setup_starting_point = data['setup_starting_point']
    formation_edge = data['formation_edge']
    #obj_success = data['obj_success']
    #obj_success_cycle = data['obj_success_cycle']
    graphCycleStart = begin_alg_time
    graphCycleEnd = total_cycle
    show_real_cycle = 0 # 0: to exclude the setup stage (stage 0) 1: to show the complete trajectory (including stage 0, meaning the setup stage)
    show_in_seconds = 1 # 0 to show in cycles 1: to show in seconds
    snapframes = 1
    #print(obj_success_cycle)
    # Extract x and y coordinates for each element
    x_positions = trajectory_data[:, 0, :]
    y_positions = trajectory_data[:, 1, :]
    x_positions_obs = obs_data[:, 0, :]
    y_positions_obs = obs_data[:, 1, :]
    x_positions_obj = obj_data[:, 0]
    y_positions_obj = obj_data[:, 1]
    x_posObsAct = posObsAct[0, :]
    y_posObsAct = posObsAct[1, :]
    x_pObjVec = pObjVec[0]
    y_pObjVec = pObjVec[1]
    
    if (fisico == 1):
        real_time_compensation = 1.45 # compensation factor due to real time delay
        # to make up for the difference so that it matches the real time (scales the
        # time step to a more accurate representation
        TIME_STEP = TIME_STEP*real_time_compensation
    
    if (show_in_seconds==1):
        escala_temp = 't (s)'
    else:
        escala_temp = 't (ciclos)'
    #print(x_positions)
    
    if (fisico == 0):
        virtualtext = f'corrida {extracted_number}, en simulación'
    
    elif (fisico == 1):
        virtualtext = f'corrida {extracted_number}, en físico'
    
    
    if (fisico == 0):
        combined_fv = 0
        texto_fisico = 'simulación'
    
    elif (fisico == 1):
        combined_fv = 1
        if (combined_fv == 1):
            pattern_f = re.compile(r'(_[hf]_)')
            # Use re.sub to replace the matched pattern with '_v_'
            filename_without_extension_v = archivo.split('.')[0]
            formatted_file = re.sub(pattern_f, '_v_', filename_without_extension_v)
        texto_fisico = 'físico'
    
    
    vx_positions = velocity_data[:, 0, :]
    vy_positions = velocity_data[:, 1, :]
    time_steps = np.arange(graphCycleStart, graphCycleEnd, 1)
    if (fisico == 1 and show_real_cycle == 0):
        time_steps = time_steps-begin_alg_time
        form_cycle = form_cycle-begin_alg_time
        obj_cycle = obj_cycle-begin_alg_time
    
    if (fisico == 0):
        form_cycle = form_cycle+1
    
    if (show_in_seconds == 1):
        time_steps = time_steps*TIME_STEP/1000
        form_cycle = form_cycle*TIME_STEP/1000
        obj_cycle = obj_cycle*TIME_STEP/1000
    #print(time_steps)
    # to match the proportions of the robotat
    plt.figure(figsize=(3.8*1.5, 4.8*1.5))
    # plotting the points 
    # trajectory
    plt.xlim(-1.9, 1.9)  # Set the x-axis limits 
    plt.ylim(-2.4, 2.4)  # Set the y-axis limits
    
    factor_m = 0.0003528 # m for each scatter point
    diam_agente = l_f # average agent diameter
    
    num_agents = x_positions.shape[1]  # Get the number of agents
    print(vx_positions.shape[1])
    print(graphCycleStart)
    print(NStart)
    print(N)
    NStart = NStart - 1
    agent_number = N-NStart
    labels = [f'Agente {i + 1}' for i in range(NStart,num_agents)] 
    #labels = [f'Agente {i}' for i in range(NStart,N+1)] 
    #NStart_calc = NStart-1
    #print(x_positions[:,NStart:N])
    
    # trajectory figure
    # __________________________________________________________________________________________________________________________________________________________________
    plt.plot(x_positions[graphCycleStart:graphCycleEnd,NStart:N], y_positions[graphCycleStart:graphCycleEnd,NStart:N], linestyle='--', zorder=4, label=labels)
    plt.scatter(x_positions[graphCycleStart,NStart:N], y_positions[graphCycleStart,NStart:N], marker='o', facecolor='none', edgecolor='red', label='Pos Iniciales', zorder=2, s = diam_agente/factor_m)
    plt.scatter(x_positions[-1,NStart:N], y_positions[-1,NStart:N], marker='o', color='green', label='Pos Finales', zorder=4, s = diam_agente/factor_m)
    plt.scatter(x_posObsAct, y_posObsAct, marker='o', color='purple', label='Obstáculos', zorder=3, s = sizeO/factor_m) # s para convertir a m
    plt.scatter(x_pObjVec, y_pObjVec, marker='*', color='yellow', label='Objetivo', zorder=2, s = 0.1/factor_m) 
    
    
    # naming the x axis
    plt.xlabel('Eje x (m)')
    # naming the y axis
    plt.ylabel('Eje y (m)')
      
    # giving a title to my graph
    plt.title(f'Trayectoria de agentes en {texto_fisico}, {extracted_value}')
    
    legend = plt.legend(markerscale=0.5)
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.31, 1))
    plt.grid()
    plt.savefig(f'finaltrials/{filename_without_extension}/traj_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/traj_{filename_without_extension}.png', format='png', bbox_inches='tight')

    print_latex_figure(f'traj_{filename_without_extension}.eps', f'Trayectoria de los {agent_number} agentes en el escenario '+f'{extracted_value}, '+ f'{virtualtext}.', f'traj_{filename_without_extension}', "0.8")
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the center of mass (cm) of the formation trajectory
    # __________________________________________________________________________________________________________________________________________________________________    
    plt.figure(figsize=(3.8*1.5, 4.8*1.5))
    # plotting the points 
    # trajectory
    plt.xlim(-1.9, 1.9)  # Set the x-axis limits
    plt.ylim(-2.4, 2.4)  # Set the y-axis limits
    
    # Scatter plot for the center of mass at every index
    plt.plot(np.mean(x_positions[graphCycleStart:graphCycleEnd, NStart:], axis=1), np.mean(y_positions[graphCycleStart:graphCycleEnd, NStart:], axis=1), linestyle='--', color='black', label='C.M. Form', zorder=5)
    
    # Scatter plot for obstacles, objective, initial positions, and final positions
    plt.scatter(x_posObsAct, y_posObsAct, marker='o', color='purple', label='Obstáculos', zorder=3, s=sizeO/factor_m)  # s para convertir a m
    plt.scatter(x_pObjVec, y_pObjVec, marker='*', color='yellow', label='Objetivo', zorder=2, s=0.1/factor_m)
    plt.scatter(x_positions[graphCycleStart,NStart:N], y_positions[graphCycleStart,NStart:N], marker='o', facecolor='none', edgecolor='red', label='Pos Iniciales', zorder=2, s = diam_agente/factor_m)
    plt.scatter(x_positions[-1, NStart:N], y_positions[-1, NStart:N], marker='o', color='green', label='Pos Finales', zorder=4, s=diam_agente/factor_m)
    # naming the x axis
    plt.xlabel('Eje x (m)')
    
    # naming the y axis
    plt.ylabel('Eje y (m)')
    
    # giving a title to the graph
    plt.title(f'Trayectoria del c.m. de la formación en {texto_fisico}, {extracted_value}')
    
    # Add legend with smaller fonts
    legend = plt.legend(markerscale=0.5)
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    # Add grid
    plt.grid()
    legend = plt.legend(markerscale=0.5)
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.31, 1))
    
    coordinate_success = graphCycleStart
    
    for coordinate in x_positions[graphCycleStart:graphCycleEnd]:
        #print(x_positions[coordinate_success, NStart])
        if (abs(np.mean(x_positions[coordinate_success, NStart:])-x_pObjVec)<0.5 and abs(np.mean(y_positions[coordinate_success, NStart:])-y_pObjVec)<0.5):
            print((coordinate_success-graphCycleStart)*TIME_STEP/1000)
            #print("******************************************************************************")
            break
        
        coordinate_success = coordinate_success+1
    
    
    # Save the plot
    plt.savefig(f'finaltrials/{filename_without_extension}/cm_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/cm_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    print_latex_figure(f'cm_{filename_without_extension}.eps', "Trayectoria del centro de masa de la formación en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'cm_{filename_without_extension}', "0.8")
    if (combined_fv == 1):
        print_latex_figure_two(f'traj_{filename_without_extension}.eps',f'traj_{formatted_file}.eps', f'Trayectoria de los {agent_number} agentes en el escenario '+ f'{extracted_value}, corrida {extracted_number} en físico (izquierda) y simulación (derecha).', f'traj_{filename_without_extension}', "0.49")
        print_latex_figure_two(f'cm_{filename_without_extension}.eps',f'cm_{formatted_file}.eps', f'Trayectoria del centro de masa de la formación en el escenario {extracted_value}, corrida {extracted_number} en físico (izquierda) y simulación (derecha).', f'cm_{filename_without_extension}', "0.49")
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the velocity norm of all agents throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________  
    plt.figure()
    plt.plot(time_steps,normV_data[graphCycleStart:graphCycleEnd])
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-40, 40])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Velocidad (m/s)')
    # giving a title to my graph
    plt.title(f'Norma de la velocidad de la formación, {texto_fisico} {extracted_value}')
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.26, 1))
    plt.savefig(f'finaltrials/{filename_without_extension}/normV_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/normV_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the mean squared error (mse) of the formation throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________  
    plt.figure()
    plt.plot(time_steps,formation_mse_data[graphCycleStart:graphCycleEnd])
    plt.axhline(y=1, color='pink', linestyle='--', label='Límite = 1')
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Unidades')
    # giving a title to my graph
    plt.title(f'Error Cuadrático Medio de la formación, {texto_fisico} {extracted_value}')
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.26, 1))
    plt.savefig(f'finaltrials/{filename_without_extension}/mse_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/mse_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    print_latex_figure_two(f'normV_{filename_without_extension}.eps',f'mse_{filename_without_extension}.eps', "Histórico de norma de velocidad de la formación y error cuadrático medio en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'normVmse_{filename_without_extension}', "0.49")
    
    if (combined_fv == 1):
        print_latex_figure_two(f'normV_{formatted_file}.eps',f'mse_{formatted_file}.eps', f'Histórico de norma de velocidad de la formación y error cuadrático medio en el escenario {extracted_value}, corrida {extracted_number}, en simulación.', f'normVmse_{formatted_file}', "0.49")
    
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the velocity of each agent throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________ 
    plt.figure()
    
    # velocityHist in x
    plt.plot(time_steps,np.sqrt(vx_positions[graphCycleStart:graphCycleEnd,NStart:N]**2+vy_positions[graphCycleStart:graphCycleEnd,NStart:N]**2), label = labels)
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-20, 20])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('V (m/s)')
      
    # giving a title to my graph
    plt.title(f'Velocidades, {texto_fisico} {extracted_value}')
    
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.26, 1))
    
    plt.grid()
    # Your plot commands here
    plt.savefig(f'finaltrials/{filename_without_extension}/vel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/vel_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the velocities in x of each agent throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________ 
    plt.figure()
    
    # velocityHist in x
    plt.plot(time_steps,vx_positions[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-20, 20])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Vx (m/s)')
      
    # giving a title to my graph
    plt.title(f'Velocidades en X, {texto_fisico} {extracted_value}')
    
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.26, 1))
    
    plt.grid()
    # Your plot commands here
    plt.savefig(f'finaltrials/{filename_without_extension}/xvel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/xvel_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the velocities in y of each agent throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________ 
    plt.figure()
    
    # velocityHist in y
    plt.plot(time_steps,vy_positions[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-20, 20])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Vy (m/s)')
      
    # giving a title to my graph
    plt.title(f'Velocidades en Y, {texto_fisico} {extracted_value}')
    
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.26, 1))
    
    plt.grid()
    plt.savefig(f'finaltrials/{filename_without_extension}/yvel_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/yvel_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    print_latex_figure_two(f'xvel_{filename_without_extension}.eps',f'yvel_{filename_without_extension}.eps', "Histórico de velocidades de los agentes en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'vel_{filename_without_extension}', "0.49")
    
    if (combined_fv == 1):
        print_latex_figure_two(f'xvel_{formatted_file}.eps',f'yvel_{formatted_file}.eps', "Histórico de velocidades de los agentes en el escenario "+f'{extracted_value}, '+ f'corrida {extracted_number}, en simulación.', f'vel_{formatted_file}', "0.49")
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # graphs the velocities in PhiL and PhiR of each agent's wheels throughout the trial
    # __________________________________________________________________________________________________________________________________________________________________ 
    plt.figure()
    
    phi = np.zeros([2,N])
    phi_data = []
    v_robot = np.zeros([1,N])
    v_robot_data = []
    #print(rot_data)
    
    for cyc in range(0, total_cycle):
        #print((rot_data[cyc][0][1]))
        
        if (fisico == 0):
            r_f = 0.0205
            l_f = 0.0355
            a_f = 0.0355
        elif (fisico == 1):   
            r_f = 0.017
            l_f = 0.0485
            a_f = 0.0485
        for argc in range(NStart,num_agents):
            v = (velocity_data[cyc][0][argc])*(math.cos(rot_data[cyc][0][argc]*math.pi/180)) + (velocity_data[cyc][1][argc])*(math.sin(rot_data[cyc][0][argc]*math.pi/180))
            w = (velocity_data[cyc][0][argc])*(-math.sin(rot_data[cyc][0][argc]*math.pi/180)/a_f) + (velocity_data[cyc][1][argc])*(math.cos(rot_data[cyc][0][argc]*math.pi/180)/a_f)
            
            # Cálculo de velocidades de las ruedas   
            phi_r = (v+(w*l_f))/r_f
            # print(phi_r)
            phi_l = (v-(w*l_f))/r_f
            # print(phi_l)
            
            # Truncar velocidades a la velocidad maxima
            if(phi_r > 0):
                if(phi_r > MAX_SPEED):
                    phi_r = MAX_SPEED
            else:
                if(phi_r < -MAX_SPEED):
                    phi_r = -MAX_SPEED
                    
            if(phi_l > 0):
                if(phi_l > MAX_SPEED):
                    phi_l = MAX_SPEED
            else:
                if(phi_l < -MAX_SPEED):
                    phi_l = -MAX_SPEED
            
            if (fisico == 0):
                phi_r = phi_r*60/(2*math.pi)
                phi_l = phi_l*60/(2*math.pi)
            phi[0][argc] = phi_r
            phi[1][argc] = phi_l
            v_robot[0][argc] = (phi_r+phi_l)*r_f/2
            phi_data.append(phi.copy())
            v_robot_data.append(v_robot.copy())
    phi_data_array = np.array(phi_data)
    v_robot_data_array = np.array(v_robot_data)
    
    phi_r_data = phi_data_array[:, 0, :]
    #print(phi_r_data)
    phi_l_data = phi_data_array[:, 1, :]
    
    v_robot_data_data = v_robot_data_array[:, 0, :]
    
    plt.plot(time_steps,phi_r_data[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-70, 70])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Phi R (rpm)')
      
    # giving a title to my graph
    plt.title(f'Velocidades R, {texto_fisico} {extracted_value}')
    
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((0.99, 1))
    plt.savefig(f'finaltrials/{filename_without_extension}/phiR_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/phiR_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    plt.figure()
    plt.plot(time_steps,phi_l_data[graphCycleStart:graphCycleEnd,NStart:N], label = labels)
    plt.axvline(x=form_cycle, color='black', linestyle='--', label=f'Inicio Form:\n{form_cycle:.2f}')
    plt.axvline(x=obj_cycle, color='yellow', linestyle='--', label=f'Seguir Obj:\n{obj_cycle:.2f}')
    plt.ylim([-70, 70])
    # naming the x axis
    plt.xlabel(f'{escala_temp}')
    # naming the y axis
    plt.ylabel('Phi L (rpm)')
    # giving a title to my graph
    plt.title(f'Velocidades L, {texto_fisico} {extracted_value}')
    
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((0.99, 1))
    plt.savefig(f'finaltrials/{filename_without_extension}/phiL_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
    plt.savefig(f'finaltrials/{filename_without_extension}/phiL_{filename_without_extension}.png', format='png', bbox_inches='tight')
    
    print_latex_figure_two(f'phiL_{filename_without_extension}.eps',f'phiR_{filename_without_extension}.eps', "Histórico de velocidades en las ruedas de los agentes en el escenario "+f'{extracted_value}, '+ f'{virtualtext}.', f'phi_{filename_without_extension}', "0.49")
    
    if (combined_fv == 1):
        print_latex_figure_two(f'phiL_{formatted_file}.eps',f'phiR_{formatted_file}.eps', "Histórico de velocidades en las ruedas de los agentes en el escenario "+f'{extracted_value}, '+ f'corrida {extracted_number}, en simulación.', f'phi_{formatted_file}', "0.49")
    
    
    # function to show the plot
    if (show_images == 1):
        plt.show()
    
    # __________________________________________________________________________________________________________________________________________________________________   
    # creates the animation gif of the whole trial
    # __________________________________________________________________________________________________________________________________________________________________ 
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(3.8*1.5, 4.8*1.5))
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-2.4, 2.4)
    
    # Initialize the scatter plots for the agents, obstacles, and goal
    scatter_agents = ax.scatter([], [], marker='o', color ='green', label='Agentes', zorder=5, s = diam_agente/factor_m)
    scatter_goal = ax.scatter([], [], marker='*', color='yellow', label='Objetivo', zorder=2, s = 0.1/factor_m)
    scatter_obstacles = ax.scatter([], [], marker='o', color='purple', label='Obstáculos', zorder=3, s = sizeO/factor_m)
    
    real_time_text = ax.text(1.03, 0.8, '', transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
    
    
    """
    total_frames = len(np.arange(graphCycleStart, graphCycleEnd, 8))
    
    snapshot_frame_1 = begin_alg_time
    snapshot_frame_2 = total_frames // 3
    snapshot_frame_3 = 2 * (total_frames // 3)
    snapshot_frame_4 = total_frames - 1
    """
    
    # Plot the initial positions
    scatter_agents.set_offsets(np.column_stack([x_positions[graphCycleStart:graphCycleEnd, NStart:N], y_positions[graphCycleStart:graphCycleEnd, NStart:N]]))
    scatter_goal.set_offsets(np.column_stack([x_positions_obj[graphCycleStart:graphCycleEnd], y_positions_obj[graphCycleStart:graphCycleEnd]]))
    scatter_obstacles.set_offsets(np.column_stack([x_positions_obs[graphCycleStart:graphCycleEnd], y_positions_obs[graphCycleStart:graphCycleEnd]]))
    
    # Function to update the scatter plots in each animation frame
    def update(frame):
        scatter_agents.set_offsets(np.column_stack([x_positions[frame, NStart:N], y_positions[frame, NStart:N]]))
        scatter_goal.set_offsets(np.column_stack([x_positions_obj[frame], y_positions_obj[frame]]))
        scatter_obstacles.set_offsets(np.column_stack([x_positions_obs[frame], y_positions_obs[frame]]))
        # Update the real-time timer in the title
            # Save equally spaced snapshots
        """    
        if (snapframes == 1):
            if frame == snapshot_frame_1:
                plt.savefig(f'finaltrials/{filename_without_extension}/snap1_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
                plt.savefig(f'finaltrials/{filename_without_extension}/snap1_{filename_without_extension}.png', format='png', bbox_inches='tight')
            elif frame == snapshot_frame_2:
                plt.savefig(f'finaltrials/{filename_without_extension}/snap2_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
                plt.savefig(f'finaltrials/{filename_without_extension}/snap2_{filename_without_extension}.png', format='png', bbox_inches='tight')
            elif frame == snapshot_frame_3:
                plt.savefig(f'finaltrials/{filename_without_extension}/snap3_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
                plt.savefig(f'finaltrials/{filename_without_extension}/snap3_{filename_without_extension}.png', format='png', bbox_inches='tight')
            elif frame == snapshot_frame_4:
                plt.savefig(f'finaltrials/{filename_without_extension}/snap4_{filename_without_extension}.eps', format='eps', bbox_inches='tight')
                plt.savefig(f'finaltrials/{filename_without_extension}/snap4_{filename_without_extension}.png', format='png', bbox_inches='tight')
        """
        real_time_seconds = frame
        if (fisico == 1 and show_real_cycle == 0):
            real_time_seconds = frame - begin_alg_time
        if (show_in_seconds == 1):
            real_time_seconds = real_time_seconds * TIME_STEP/1000
            #plt.title(f'Trayectorias - Tiempo Real: {real_time_seconds:.2f} segundos')
            real_time_text.set_text(f'Tiempo Real: \n{real_time_seconds:.2f} s')
        else:
            real_time_seconds = frame
            #plt.title(f'Trayectorias - Tiempo Real: {real_time_seconds} ciclos')
            real_time_text.set_text(f'Tiempo Real: \n{real_time_seconds} ciclos')
    
    
    # Create the animation
    animation = FuncAnimation(fig, update, frames=np.arange(graphCycleStart, graphCycleEnd, 8), interval = 50, blit=False)
    
    # Display the plot
    plt.xlabel('Eje x (m)')
    plt.ylabel('Eje y (m)')
    plt.title(f'Trayectoria de corrida en {texto_fisico}, {extracted_value}')
    legend = plt.legend(markerscale=0.5)
    for text in legend.get_texts():
        text.set_fontsize(7)
    
    # Generating the output GIF filename based on the input filename
    output_gif_filename = f'finaltrials/{filename_without_extension}/animation_{filename_without_extension}.gif'
    # Saving the animation with the dynamically generated filename
    animation.save(output_gif_filename, writer='Pillow')
    plt.subplots_adjust(right=0.8)
    legend.set_bbox_to_anchor((1.3, 1))
    plt.grid()
    if (show_images == 1):
        plt.show()
    
    
    
        