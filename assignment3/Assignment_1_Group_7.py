import sys

"""
Gap costs (Insertion / Deletion)
"""
gap_cost = -8

"""
Function to create a matrix as a list
"""
def create_matrix(rows, cols):
    matrix = [[0 for col in range(cols)] for row in range(rows)]

    return matrix


"""
Creates the replacement cost matrix

Unfortunately this is hardcoded as we ran out of time to parse the txt
"""
def create_replacement_cost_matrix():
    """matrix = [{}, {}]
    with open("matrix.txt") as file:
        for line in file:
            if line.startswith("#") == False:
                if """
            
    return [[5, -3, -4, -4], [-3, 5, -4, -4],
            [-4, -4, 5, -2], [-4, -4, -2, 5]]


"""
Takes score values and their neighbors from our matrix and adds the (gap) costs

Returns the maximum of those values
"""
def calculate_score(matrix, cost, x, y):
    diag_score = matrix[x - 1][y - 1] + cost
    up_score = matrix[x - 1][y] + gap_cost
    left_score = matrix[x][y - 1] + gap_cost

    return max(0, diag_score, up_score, left_score)


"""
Method to calculate the next move based on our score matrix 
"""

def calc_next_move(score_matrix, x, y):
    diag = score_matrix[x - 1][y - 1]
    up = score_matrix[x - 1][y]
    left = score_matrix[x][y - 1]

    if diag >= up and diag >= left:
        return 1 if diag != 0 else 0
    elif up > diag and up >= left:
        return 2 if up != 0 else 0
    elif left > diag and left > up:
        return 3 if left != 0 else 0


"""
Traceback method which determines the best way through the matrix
Gaps are replaced with '-'

Returns the sequences, amount of matches, miss_matches and deletions
"""
def traceback(score_matrix, start_pos, seq1, seq2):
    matches = 0
    miss_matches = 0
    deletions = 0
    aligned_seq1 = []
    aligned_seq2 = []
    x, y = start_pos
    move = calc_next_move(score_matrix, x, y)
    while move != 0:
        if move == 1:
            if seq1[x - 1] == seq2[y - 1]:
                matches += 1
            else:
                miss_matches += 1
            aligned_seq1.append(seq1[x - 1])
            aligned_seq2.append(seq2[y - 1])
            x -= 1
            y -= 1
        elif move == 2:
            aligned_seq1.append(seq1[x - 1])
            aligned_seq2.append("-")
            deletions += 1
            x -= 1
        else:
            aligned_seq1.append("-")
            aligned_seq2.append(seq2[y - 1])
            deletions += 1
            y -= 1

        move = calc_next_move(score_matrix, x, y)
    aligned_seq1.append(seq1[x - 1])
    aligned_seq2.append(seq2[y - 1])

    return "".join(reversed(aligned_seq1)), "".join(reversed(aligned_seq2)), matches, miss_matches, deletions

"""
Calculates the alignment table, the maximum position and the max_score

These values are later used for the traceback
"""
def calculate_sw_table(seq1, seq2, cost_matrix, gap_cost):
    alignment_table = create_matrix(len(seq1) + 1, len(seq2) + 1)
    lookup_indexes = {"a": 0, "t": 1, "g": 2, "c": 3}  
    max_score = 0
    max_pos = None

    for i in range(1, len(alignment_table)):
        for j in range(1, len(alignment_table[i])):
            score = calculate_score(alignment_table, cost_matrix[lookup_indexes[seq1[i - 1].lower()]][lookup_indexes[seq2[j - 1].lower()]], i - 1, j - 1)
            if score > max_score:
                max_score = score
                max_pos = (i, j)
            
            alignment_table[i - 1][j - 1] = score
    
    return alignment_table, max_pos, max_score

            
def main(args):
    # getting the template_file path from command line and try to parse it
    try:
        template_file = open(args[0], "r")
    except Exception as exception:
        print("Something went wrong while parsing fast template: " + repr(exception))
        sys.exit(-1)

    sequences = []
    buffer = ""
    for line in template_file:
        if line.startswith(">") == False:
            buffer += line.strip("\n")
        else:
            if buffer != "":
                sequences.append(buffer)
                buffer = ""
    
    sequences.append(buffer)

    template_file.close()

    score_matrix, max_pos, max_score = calculate_sw_table(sequences[0], sequences[1], create_replacement_cost_matrix(), 8)
    seq1, seq2, matches, miss_matches, deletions = traceback(score_matrix, max_pos, sequences[0], sequences[1])

    print("Alignment score: {}".format(max_score))
    print("Matches: {}".format(matches))
    print("Mismatches: {}".format(miss_matches))
    print("Insertions/Deletions: {}".format(deletions))
    print("Length: {}".format(0))
    print(seq1)
    print(seq2)
    

if __name__ == '__main__':
    main(sys.argv[1:])