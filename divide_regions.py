import os

a = 2.99
n = 15
crack = 5

# Define variables to store the values
xlo = None
xhi = None
ylo = None
yhi = None
zhi = None

# Open the file
with open("NVE.data", "r") as file:
    # Read lines from the file
    lines = file.readlines()
    
    # Iterate over each line
    for line in lines:
        # Split the line by whitespace
        parts = line.split()
        
        # Check if the line contains xlo xhi values
        if len(parts) >= 4 and parts[2] == 'xlo' and parts[3] == 'xhi':
            xlo = float(parts[0])
            xhi = float(parts[1])
        # Check if the line contains ylo yhi values
        elif len(parts) >= 4 and parts[2] == 'ylo' and parts[3] == 'yhi':
            ylo = float(parts[0])
            yhi = float(parts[1])
        elif len(parts) >= 4 and parts[2] == 'zlo' and parts[3] == 'zhi':
            zhi = float(parts[1])

volume = ((xhi - xlo)*(yhi - ylo)*zhi) - (4*a-xlo)*4*a*zhi
print('volume of the system is ',volume)

# Initialize x1_start as the starting x value
x1_start = ((crack-1)*a)+xlo

# Calculate the width of each zone
x_width  = (xhi-x1_start)/n

# Calculate y2
y2 = (ylo + yhi) / 2

# Initialize zone count
zone_count = 0

# Initialize file count
file_count = 1

# Function for writing the initial commands
def write_initial_commands(file):
    file.write("# CZM separation zone atom data extraction\n")
    file.write("\n")
    file.write("# [Initialization\n")
    file.write("package omp 4\n")
    file.write("units metal\n")
    file.write("atom_style atomic\n")
    file.write("dimension 3\n")
    file.write("boundary s s p\n")
    file.write("\n")
    file.write("# [Loading restart file from the NVT-NVE stabilization\n")
    file.write("read_data NVE.data\n")
    file.write("\n")
    file.write("# [Force fields\n")
    file.write("pair_style meam\n")
    file.write("pair_coeff * * library.meam Co Ti CoTi.meam Co Ti\n")
    file.write("\n")


# Ff the dumps directory is not present then create it. 
if not os.path.exists("./dumps"):
    os.makedirs("./dumps")

# Open a file to save the regions
with open(f"CZM_{file_count}.lammps", "w") as file:
    # Write the initial commands
    file.write("# CZM separation zone atom data extraction\n")
    file.write("\n")
    file.write("# [Initialization\n")
    file.write("package omp 4\n")
    file.write("units metal\n")
    file.write("atom_style atomic\n")
    file.write("dimension 3\n")
    file.write("boundary s s p\n")
    file.write("\n")
    file.write("# [Loading restart file from the NVT-NVE stabilization\n")
    file.write("read_data NVE.data\n")
    file.write("\n")
    file.write("# [Force fields\n")
    file.write("pair_style meam\n")
    file.write("pair_coeff * * library.meam Co Ti CoTi.meam Co Ti\n")
    file.write("\n")

    file.write("# Making the cohesive zone cells at +-0.5a from the interface line and dumping the position and id of the atoms\n")
    for i in range(1, n+1):
        # Calculate x1 and x2 for the current zone
        x1 = x1_start + (i - 1) * x_width
        x2 = x1_start + i * x_width
        
        # Write the region formatting to the file
        file.write(f"region {i} block {x1} {x2} {y2 - 3*a} {y2 + 3*a} 0 {zhi}\n")
        file.write(f"group {i} region {i}\n")
        file.write(f"dump {i} {i} custom 1 ./dumps/{i}.dump id x y z\n")

        # Increment the zone count
        zone_count += 1
        
        # If zone count reaches 10, close the current file and open a new one
        if zone_count == 10:
            # Write the run command at the end of the file
            file.write("run 0")
            file.close()
            file_count += 1
            zone_count = 0
            file = open(f"CZM_{file_count}.lammps", "w")
            write_initial_commands(file)

    # print this on the last file
    file.write("run 0")

# Print a message
print("Lammps scripts for CZM have been created successfully")



