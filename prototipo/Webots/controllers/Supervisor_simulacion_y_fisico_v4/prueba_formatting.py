import re

initial_conditions_file = 'finaltrial_6A_AAA_h_2.npz'

# Define a regular expression pattern to match either "_h_" or "_f_"
pattern = re.compile(r'(_[hf]_)')

# Use re.sub to replace the matched pattern with '_v_'
formatted_file = re.sub(pattern, '_v_', initial_conditions_file)

print(formatted_file)