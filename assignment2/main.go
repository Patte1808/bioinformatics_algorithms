package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
)

/*
	Small helper function to panic in case of errors
*/
func check(e error) {
	if e != nil {
		panic(e)
	}
}

/*
	Creates the bad character table
*/
func makeBadCharacterTable(pattern string) map[string] int {
	//patternLength := len(pattern)
	badCharacterTable := make(map[string] int)
	charactersInPattern := strings.Split(pattern, "")

	sortedCharactersArr :=strings.Split(pattern, "")
	sort.Strings(sortedCharactersArr)
	sortedCharactersString := strings.Join(sortedCharactersArr, "")

	for index := range sortedCharactersString {
		char := charactersInPattern[index]

		badCharacterTable[char] = index
	}

	return badCharacterTable
}

/*
	Small helper function to calculate the maximum of 2 ints
*/
func max(x, y int) int {
	if x < y {
		return y
	}

	return x
}

/*
	Small helper function to calculate the minimum of 2 ints
 */
func min(x, y int) int {
	if x > y {
		return y
	}

	return x
}

/*
	boyerMoore takes a pattern string and the template string.
	It then searches for all occurences of this pattern in our template string

	returns an array of all matches and an occurence counter
 */
func boyerMoore(pattern string, text string) ([]int, int) {
	matches := make([]int, 0)
	patternLength := len(pattern)
	textLength := len(text)
	occurenceCounter := 0

	if patternLength > textLength {
		return matches, occurenceCounter
	}

	badMatchTable := makeBadCharacterTable(pattern)
	shift := 0

	for shift <= textLength - patternLength {
		index := patternLength - 1

		for index >= 0 && pattern[index] == text[shift + index] {
			index -= 1
		}

		if index < 0 {
			matches = append(matches, shift)
			occurenceCounter += 1

			if shift + patternLength < textLength {
				shift += patternLength - badMatchTable[string(text[shift + patternLength])]
			} else {
				shift += 1
			}
		} else {
			shift += max(1, index - badMatchTable[string(text[shift + index])])
		}
	}

	return matches, occurenceCounter
}

/*
	parsePatternFile expects a filepath
	it then parses a (fasta) pattern file, cleans it by removing all newlines and returns an array of patterns
*/
func parsePatternFile(filepath string) []string {
	file, err := os.Open(filepath)

	// In case there's an error while opening a file, we panic.
	check(err)
	defer file.Close()

	patterns := []string{}
	scanner := bufio.NewScanner(file)

	// we use a scanner to read the files content line by line
	for scanner.Scan() {
		currentLine := scanner.Text()

		// Skip the non-sense
		if currentLine[0] != '>' {
			patterns = append(patterns, currentLine)
		}
	}

	return patterns
}

/*
	parseTemplateFile expects a filepath
	it then parses a (fasta) template file, cleans it by removing all newlines and returns the template as a string
*/
func parseTemplateFile(filepath string) string {
	templateString := ""

	// This will read the whole file in-memory
	// in low memory environments, this could potentially cause OOM exceptions (but Gruenau is strong)
	data, err := ioutil.ReadFile(filepath)

	// In case there's an error while opening a file, we panic.
	check(err)
	templateString = string(data)
	// Template file always starts with non-sense, we skip this part here
	templateString = templateString[1:]
	templateString = strings.ReplaceAll(templateString, "\n", "")

	return templateString
}

func main() {
	// take all command line arguments except the file name of the program
	args := os.Args[1:]

	// check: are there at least 2 command line args?
	if len(args) < 2 {
		// raise error as we need 2 command line args (pattern and template)
		panic("Not enough command line arguments")
	}

	patterns := parsePatternFile(args[0])
	templateString := parseTemplateFile(args[1])

	for pattern := range patterns {
		matches, occurences := boyerMoore(patterns[pattern], templateString)
		fmt.Println(patterns[pattern], ": ", occurences)

		takePositionsUntil := min(10, len(matches))
		fmt.Println("Matching positions: ", matches[:takePositionsUntil])
	}
}