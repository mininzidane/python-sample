import itertools

def parse_label_coordinates_map(file_path: str) -> dict:
    label_coordinates_map = {}
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                line = eval(line.strip())
                if line[3] not in label_coordinates_map:
                    label_coordinates_map[line[3]] = []
                label_coordinates_map[line[3]].append((line[0:3], i))

        return label_coordinates_map

    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_min_volume_indexes(label_coordinates_map: dict) -> tuple:
    min_volume = float('inf')
    min_indexes = None
    for label, coordinates in label_coordinates_map.items():
        if len(coordinates) < 4:
            continue
        for combination in itertools.combinations(range(len(coordinates)), 4):
            (p1, i1), (p2, i2), (p3, i3), (p4, i4) = [coordinates[i] for i in combination]
            current_volume = volume_of_tetrahedron(p1, p2, p3, p4)
            if current_volume < min_volume:
                min_volume = current_volume
                min_indexes = (i1, i2, i3, i4)

    return min_indexes

def volume_of_tetrahedron(p1, p2, p3, p4):
    # Vectors from p1 to p2, p3, and p4
    AB = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    AC = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    AD = (p4[0] - p1[0], p4[1] - p1[1], p4[2] - p1[2])

    # Direct calculation of the cross product components
    cross_product_x = AB[1] * AC[2] - AB[2] * AC[1]
    cross_product_y = AB[2] * AC[0] - AB[0] * AC[2]
    cross_product_z = AB[0] * AC[1] - AB[1] * AC[0]

    # Dot product of AD with the cross product of AB and AC
    scalar_triple_product = (
        AD[0] * cross_product_x +
        AD[1] * cross_product_y +
        AD[2] * cross_product_z
    )

    # The volume of the tetrahedron
    volume = abs(scalar_triple_product) / 6.0
    return volume

# Example points
# A = (1, 2, 3)
# B = (2, 3, 4)
# C = (1, 5, 1)
# D = (4, 2, 3)

# Calculate the volume
# vol = volume_of_tetrahedron(A, B, C, D)
# print(f"The volume of the tetrahedron is {vol}")

label_coordinates_map = parse_label_coordinates_map('points_small.txt')
indexes = find_min_volume_indexes(label_coordinates_map)
print(indexes)
print(volume_of_tetrahedron((385.51, 286.94, 209.29), (252.56, 15.42, 153.79), (65.04, 56.84, 133.9), (411.94, 210.46, 202.43))) #527.17 (CORRECT)

label_coordinates_map = parse_label_coordinates_map('points_large.txt')
# indexes = find_min_volume_indexes(label_coordinates_map)
# print(indexes) #(244, 587, 654, 3248)
print(volume_of_tetrahedron((310.87, 375.57, 462.46), (212.47, 392.18, 164.87), (240.88, 354.2, 286.49), (232.81, 347.73, 270.51))) #0.028878 (CORRECT)
