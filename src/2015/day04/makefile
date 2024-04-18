CC=gcc
CFLAGS=-Wall
LIBS=-lssl -lcrypto
TARGET=solution

all: $(TARGET)

$(TARGET): solution.c
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(TARGET)
