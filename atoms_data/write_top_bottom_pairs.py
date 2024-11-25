# Function to extract the atom ids and their position as NumPy arrays
def extract_atom_data(file_name):
    # Initialize lists to store IDs and positions
    atom_id_position = []

    # Open the file for reading
    with open(file_name, 'r') as file:
        # Variable to track whether we are currently reading atom data
        reading_atoms = False

        # Iterate through each line in the file
        for line in file:
            line = line.strip()

            # Check if we are starting to read atom data
            if line == "ITEM: ATOMS id x y z":
                reading_atoms = True
                continue

            # If we are reading atom data, split the line and extract ID and position
            if reading_atoms:
                atom_data = line.split()
                if len(atom_data) == 4:
                    atom_id = int(atom_data[0])
                    x, y, z = map(float, atom_data[1:4])
                    atom_id_position.append((atom_id, [x, y, z]))
                else:
                    # Break the loop if we are done reading atom data
                    break

    # Return a list of atom IDs and a list of atom positions as NumPy arrays
    return atom_id_position


def find_top_bottom_atoms(atom_data):
    top_atom = None
    bottom_atom = None
    ymax = 0
    ymin = 9999

    for atom_id, atom_position in atom_data:
        if atom_position[1] < ymin:
            bottom_atom = atom_id
            ymin = atom_position[1]
        if atom_position[1] > ymax:
            top_atom = atom_id
            ymax = atom_position[1]
    return top_atom, bottom_atom


# Read all the Cohesive zone dump file pairs and read the pairs with minimum distances
def write_top_bottom_atoms(n, input_folder, output):
    measured_atoms = ''
    with open(output, "w") as file_to_write:
        for i in range(1,n+1):
            file = f'{input_folder}/{i}.dump'
            top, bottom = find_top_bottom_atoms(extract_atom_data(file))
            if(top):
                file_to_write.write(f'{i} {top} {bottom}\n')
                measured_atoms += f'{top} {bottom} '
                
    with open('measured_atoms.txt', 'w') as measured:
        measured.write(measured_atoms)


# Call the function to save the pair ids
n = 15 # Number of cohesive cells
input_folder = "../dumps/"
output  = "top_bottom_atom_pairs.txt"
write_top_bottom_atoms(n, input_folder, output)
print('Successfully wrote the top and bottom pairs')