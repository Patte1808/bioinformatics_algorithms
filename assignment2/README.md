# Compile
Compile the assignment using `go build main.go`

# Command line args
The program expects 2 command line arguments.
The first argument is the patterns file, the second is the template file

`./main ./Patterns.fasta ./Template.fasta`

or 

`go run main.go ./Patterns.fasta ./Template.fasta`

If there's less than 2 command line args, the program will stop with a panic message.