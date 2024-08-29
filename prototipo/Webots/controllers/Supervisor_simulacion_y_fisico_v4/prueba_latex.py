def print_latex_figure(filename, caption, label, width):
    latex_code = f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width={width}\\textwidth]{{figuras/{filename}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""

    print(latex_code)

# Example usage
print_latex_figure("modelo3_fisico_C5A_1_traj1", "Trayectoria de los 5 agentes a partir de las marcas iniciales.", "modelo3_fisico_C5A_1_traj1", "0.75")
