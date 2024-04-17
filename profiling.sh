export PATH=$PATH:/home/wjy/pmu-tools
if [ $# = 1 ]; then
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic2.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_cache0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_cache1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_floating_point0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_frontend0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_memory0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_memory1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_other0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_pipeline0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_pipeline1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory2.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory3.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory4.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory5.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory6.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory7.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory8.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory9.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory10.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory11.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory12.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory13.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory14.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory15.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory16.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory17.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory18.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory19.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory20.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory21.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory22.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory23.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory24.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory25.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory26.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory27.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory28.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory29.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory30.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory31.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches0.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches1.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches2.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches3.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches4.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches5.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches6.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches7.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches8.txt
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches9.txt
fi
if [ $# = 2 ]; then
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_basic2.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_cache0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_cache1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_floating_point0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_frontend0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_memory0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_memory1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_other0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_pipeline0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_pipeline1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory2.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory3.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory4.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory5.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory6.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory7.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory8.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory9.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory10.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory11.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory12.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory13.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory14.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory15.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory16.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory17.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory18.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory19.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory20.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory21.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory22.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory23.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory24.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory25.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory26.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory27.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory28.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory29.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory30.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_virtual_memory31.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches0.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches1.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches2.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches3.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches4.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches5.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches6.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches7.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches8.txt --benchmark $2
	python perf.py $1 -e extracted_list/ocperf_list_extracted_Unknown_Branches9.txt --benchmark $2
fi
