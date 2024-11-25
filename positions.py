import math


# Function to parse the measured_atoms
def get_measured_atoms(file_name):
    with open(file_name) as file:
        return file.readline().split()
    
# Function to make dictionary according to measured atoms
def make_atoms_dictionary(measured_atoms):
    atoms_dictionary = {}
    for atom in measured_atoms:
        atoms_dictionary[atom] = []
    return atoms_dictionary

# Function to save cellwise position data
def save_position_data(measured_atoms, data):
    cell_no = 1
    for i in range(0, len(measured_atoms), 2):
        initial_distance = data[measured_atoms[i]][0][1][1] - data[measured_atoms[i+1]][0][1][1]
        with open(f'positions/{cell_no}.txt','w') as file:
            for id, info in enumerate(data[measured_atoms[i]]):
                timestep = info[0]
                distance = data[measured_atoms[i]][id][1][1] - data[measured_atoms[i+1]][id][1][1] - initial_distance
                file.write(f'{timestep} {distance}\n')
        cell_no += 1
            


# Function to parse data from a string
def parse_data(datafile, measured_atoms_file):
    with open(datafile) as data:
        lines = data.readlines()

        measured_atoms = get_measured_atoms(measured_atoms_file)
        atoms_dictionary = make_atoms_dictionary(measured_atoms)
        
        # Iterate over lines
        i = 0
        while i < len(lines):
            # Check for TIMESTEP header
            if lines[i].startswith("ITEM: TIMESTEP"):
                timestep = int(lines[i + 1])
                num_atoms = int(lines[i + 3])

                # Extract atom coordinates
                for j in range(i + 9, i + 9 + num_atoms):
                    atom_info = lines[j].split()
                    atom_id = atom_info[0]
                    if atom_id in measured_atoms:
                        coords = list(map(float, atom_info[2:5]))
                        atoms_dictionary[str(atom_id)].append([timestep, coords])


                # Move to the next TIMESTEP
                i += 9 + num_atoms
            else:
                # Move to the next line
                i += 1

    return atoms_dictionary


# Call the functions
measured_atoms_file = 'atoms_data/measured_atoms.txt'
datafile = '../output/co_ti.300k.lammpstrj'

data = parse_data(datafile, measured_atoms_file)
save_position_data(get_measured_atoms(measured_atoms_file), data)
