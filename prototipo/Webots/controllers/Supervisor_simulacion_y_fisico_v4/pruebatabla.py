from prettytable import PrettyTable

# Create a PrettyTable object
table = PrettyTable()

# Define the table columns
columns = ["Name", "Age", "City"]
table.field_names = columns

# Add data to the table
table.add_row(["John", 25, "New York"])
table.add_row(["Jane", 30, "San Francisco"])
table.add_row(["Bob", 22, "Chicago"])
table.add_row(["Bob", 22, "Chicago"])

# Get the LaTeX code for the table
latex_code = table.get_latex_string()

# Determine the number of rows and columns
num_rows = len(table._rows)
num_columns = len(columns)

# Generate the LaTeX code with a full grid
latex_code_with_full_grid = ("\\begin{tabular}{|" + "|".join(["c"] * num_columns) + "|}\n\\hline\n"+ latex_code.replace("\\begin{tabular}", "").replace("\\end{tabular}", "").replace("&", " & ").replace("\\\\", " \\\\ \\hline\n") +"\\hline\n\\end{tabular}")

# Print the LaTeX code with a full grid
print(latex_code_with_full_grid)