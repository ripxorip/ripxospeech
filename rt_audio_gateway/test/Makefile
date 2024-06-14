# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -I../inc -I../src -I../../rt_audio_common

# Source files
SRC = $(filter-out ../src/main.c, $(wildcard ../src/*.c)) $(wildcard *.c)

# Test files
TESTS = $(wildcard *.c)

# Output executable
OUT = run_tests

all: $(SRC) $(TESTS)
	$(CC) $(CFLAGS) $^ -o $(OUT)

clean:
	rm -f $(OUT)