import sys

"""
Trie data structure

end_of_trie = end of a leaf in our Trie. Similiar to red-black-trees NIL-leaf

Input: takes a list of patterns to build up the Trie
"""
class Trie:
    end_of_trie = '$end$'
    root = dict()

    def __init__(self, *patterns):
        for word in patterns:
            current_dict = self.root
            for char in word:
                current_dict = current_dict.setdefault(char, {})
            current_dict[self.end_of_trie] = self.end_of_trie
    
    """
    Input:
    word - the word to check against our patterns
    occurence_counter - dict which counts how often a pattern from the Trie was matched
    current_absolute_position - the current absolute position in our fast-file
    matching_positions - dict of (absolute) positions where our pattern was matched
    """
    def find_word_in_trie(self, word, occurence_counter, current_absolute_position, matching_positions):
        # Start from the root of our Trie
        current_dict = self.root

        # we use this to match sub-words of the given word
        current_trie_search = ''
        
        # iterate through every character
        for char in word:

            # if is end-leaf, we found a match
            # This can either be a sub-word or the full word, we don't care
            if self.end_of_trie in current_dict:
                occurence_counter[current_trie_search] += 1

            # We only want the first 10 matching positions for this pattern
                if occurence_counter[current_trie_search] < 10:
                    if len(matching_positions[current_trie_search]) > 0:
                        matching_positions[current_trie_search] += ", "
                    
                    # Add the absolute-position for the current matched word
                    matching_positions[current_trie_search] += "{}".format(str(current_absolute_position))

            # if char is in our current dict
            if char in current_dict:
                # we have to go deeper
                current_dict = current_dict[char]

                # Add the current char to our current matching search string from the trie
                current_trie_search += char
            # char is not part of our Trie, we can abort
            else:
                return False
        # in case there's nothing left to iterate through
        else: 
            # Check one last time whether we might have a match
            if self.end_of_trie in current_dict:
                # Logic same as above, could be refactored to one method, but we didn't do that.
                occurence_counter[current_trie_search] += 1
                if occurence_counter[current_trie_search] < 10:
                    if len(matching_positions[current_trie_search]) > 0:
                        matching_positions[current_trie_search] += ", "
                    matching_positions[current_trie_search] += "{}".format(str(current_absolute_position))
                return True
            # It's neither the end of our Trie, nor do we have anything to iterate over anymore
            # I don't think this case can ever happen except if our Trie is empty, but one has to be sure.
            else:
                return False


# Parse patterns, ignore beginning of sequence and replace line breaks
def parse_patterns(file_stream):
    patterns = []
    for line in file_stream:
        if line[0] != '>':
            patterns.append(line.replace("\n", "").lower())

    file_stream.close()
    
    return patterns
            

def main(args):
    # getting the template_file path from command line and try to parse it
    try:
        template_file = open(args[0], "r")
    except Exception as exception:
        print("Something went wrong while parsing fast template: " + repr(exception))
        sys.exit(-1)
    
    # getting the pattern_file path from command line and try to parse it
    try:
        pattern_file = open(args[1], "r")
    except:
        print("Invalid pattern file")
        sys.exit(-1)

    # parse le file del patterns
    patterns = parse_patterns(pattern_file)

    # create trie
    trie = Trie(*patterns)

    # create occurence counter to count patterns
    # create matching positions dicts to print the absolute positions of occurences later
    occurence_counter = {}
    matching_positions = {}

    for pattern in patterns:
        occurence_counter[pattern] = 0
        matching_positions[pattern] = ""

    # get the maxiumum length of our patterns
    # this is the 'mask' we're using to iterate over the fasta content (see more in doc)
    # btw lessons learned here: 
    # to get the correct maximum, one has to specify a key which is being used to get the maximum.
    max_pattern_len = len(max(patterns, key = len))

    # There might be some leftovers if the line is shorter than our 
    surplus = ""
    enough_characters = True

    # the absolute character position
    current_absolute_position = 0

    for line in template_file:
        # get rid of fckn line breaks lol and to lower
        line = line.replace("\n", "").lower()

        # skip beginning of sequence
        if line[0] != '>':
            start_index = 0
            end_index = start_index + max_pattern_len
            enough_characters = True

            if surplus != "":
                # appending surplus to current line
                line = surplus + line

                # clean up surplus buffer
                surplus = ""

            # as long as we have enough characters to cover our max_pattern_len we're good to go
            while enough_characters:
                if line[start_index:end_index] and len(line[start_index:end_index]) >= max_pattern_len:
                    trie.find_word_in_trie(line[start_index:end_index], occurence_counter, current_absolute_position, matching_positions)
                    
                    # Build new 'search'-mask
                    start_index += 1
                    end_index += 1
                # our build up mask doesn't fit into the current line, we're done with this line
                else:
                    # reached end of line
                    surplus = line[start_index:]
                    enough_characters = False
                
                current_absolute_position += 1

    # Just to be sure:
    # if we read the last line and there's still a surplus, we need check whether there might be a pattern-match in this surplus
    if len(surplus) > 0:
        for i in range(len(surplus)):
            # cut the string from the beginning until the end
            # this way we make sure that we still check for patterns in our surplus
            print("There is a surplus {}".format(surplus[i:]))
            trie.find_word_in_trie(surplus[i:], occurence_counter, current_absolute_position, matching_positions)

    # print out patterns and their occurence counter / positions
    for pattern in patterns:
        print("{}: {}".format(pattern, occurence_counter[pattern]))
        print("Matches occur at positions: [{}]".format(matching_positions[pattern]))

    template_file.close()


if __name__ == '__main__':
    main(sys.argv[1:])