package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func makeBadMatchTable(pattern string) map[string] int {
	//patternLength := len(pattern)
	badMatchTable := make(map[string] int)
	charactersInPattern := strings.Split(pattern, "")

	sortedCharactersArr :=strings.Split(pattern, "")
	sort.Strings(sortedCharactersArr)
	sortedCharactersString := strings.Join(sortedCharactersArr, "")

	for index := range sortedCharactersString {
		char := charactersInPattern[index]

		badMatchTable[char] = index
	}

	return badMatchTable
}

func max(x, y int) int {
	if x < y {
		return y
	}

	return x
}

func boyerMoore(pattern string, text string) ([]int, int) {

	matches := make([]int, 0)
	patternLength := len(pattern)
	textLength := len(text)
	occurenceCounter := 0

	if patternLength > textLength {
		return matches, occurenceCounter
	}

	badMatchTable := makeBadMatchTable(pattern)
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

func parsePatternFile(filepath string) []string {
	file, err := os.Open(filepath)
	check(err)
	defer file.Close()

	patterns := []string{}
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		currentLine := scanner.Text()

		if currentLine[0] != '>' {
			patterns = append(patterns, currentLine)
		}
	}

	return patterns
}

func parseTemplateFile(filepath string) string {
	templateString := ""

	data, err := ioutil.ReadFile(filepath)
	check(err)
	templateString = string(data)
	templateString = templateString[1:]
	templateString = strings.ReplaceAll(templateString, "\n", "")

	return templateString
}

func main() {
	patterns := parsePatternFile("./Search_patterns.fasta")
	templateString := parseTemplateFile("./Template_Chr_20.fasta")

	for pattern := range patterns {
		matches, occurences := boyerMoore(patterns[pattern], templateString)
		fmt.Println(patterns[pattern], ": ", occurences)
		fmt.Println("Matching positions: ", matches[:10])
	}
}