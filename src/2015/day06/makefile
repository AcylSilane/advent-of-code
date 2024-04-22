FC=gfortran
FFLAGS=-std=legacy -Wall -O3 -march=native
TARGET=solution

all: $(TARGET)

$(TARGET): solution.f
	$(FC) $(FFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)