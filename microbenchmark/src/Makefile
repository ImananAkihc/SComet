all: microbench microbench_pollu microbench_ran
microbench: microbench.cpp
	g++ -std=c++11 -O3 -o $@ $@.cpp
microbench_pollu: microbench_pollu.cpp
	g++ -std=c++11 -O3 -o $@ $@.cpp
microbench_ran: microbench_ran.cpp
	g++ -std=c++11 -O3 -o $@ $@.cpp

clean: 
	rm -rf microbench microbench_pollu microbench_ran
