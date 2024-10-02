mkdir -p type1_runs
mkdir -p type2_runs

start_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
echo $start_date_time;

# Type 1 runs
# Effect of Client Count. Fix dataset size to 2^19, duplication percentage to 30% and vary client count in [10,20,30,40,50]
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 524288 --dup-per 0.3 > type1_runs/19_10_0.3.log
python ../main_int.py --psi-type 1 --num-clients 20 --num-ele 524288 --dup-per 0.3 > type1_runs/19_20_0.3.log
python ../main_int.py --psi-type 1 --num-clients 30 --num-ele 524288 --dup-per 0.3 > type1_runs/19_30_0.3.log
python ../main_int.py --psi-type 1 --num-clients 40 --num-ele 524288 --dup-per 0.3 > type1_runs/19_40_0.3.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 524288 --dup-per 0.3 > type1_runs/19_50_0.3.log

# Effect of Dataset size. Fix client to count to 50, duplication percentage to 30% and vary dataset size in [2^10, 2^11, 2^13, 2^15, 2^17, 2^19]
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 1024 --dup-per 0.3 > type1_runs/10_50_0.3.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 2048 --dup-per 0.3 > type1_runs/11_50_0.3.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 8192 --dup-per 0.3 > type1_runs/13_50_0.3.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 32768 --dup-per 0.3 > type1_runs/15_50_0.3.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 131072 --dup-per 0.3 > type1_runs/17_50_0.3.log


# Effect of duplication percentage. Fix client count to 50, datasize size to 2^19, and vary duplication percentage in [10%, 30%, 50%, 70%, 90%]
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 524288 --dup-per 0.1 > type1_runs/19_50_0.1.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 524288 --dup-per 0.5 > type1_runs/19_50_0.5.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 524288 --dup-per 0.7 > type1_runs/19_50_0.7.log
python ../main_int.py --psi-type 1 --num-clients 50 --num-ele 524288 --dup-per 0.9 > type1_runs/19_50_0.9.log


# Type 2 runs
# Effect of Client Count. Fix dataset size to 2^19, duplication percentage to 30% and vary client count in [10,20,30,40,50]
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 524288 --dup-per 0.3 > type2_runs/19_10_0.3.log
python ../main_int.py --psi-type 2 --num-clients 20 --num-ele 524288 --dup-per 0.3 > type2_runs/19_20_0.3.log
python ../main_int.py --psi-type 2 --num-clients 30 --num-ele 524288 --dup-per 0.3 > type2_runs/19_30_0.3.log
python ../main_int.py --psi-type 2 --num-clients 40 --num-ele 524288 --dup-per 0.3 > type2_runs/19_40_0.3.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 524288 --dup-per 0.3 > type2_runs/19_50_0.3.log

# Effect of Dataset size. Fix client to count to 50, duplication percentage to 30% and vary dataset size in [2^10, 2^11, 2^13, 2^15, 2^17, 2^19]
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 1024 --dup-per 0.3 > type2_runs/10_50_0.3.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 2048 --dup-per 0.3 > type2_runs/11_50_0.3.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 8192 --dup-per 0.3 > type2_runs/13_50_0.3.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 32768 --dup-per 0.3 > type2_runs/15_50_0.3.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 131072 --dup-per 0.3 > type2_runs/17_50_0.3.log

# Effect of duplication percentage. Fix client count to 50, datasize size to 2^19, and vary duplication percentage in [10%, 30%, 50%, 70%, 90%]
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 524288 --dup-per 0.1 > type2_runs/19_50_0.1.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 524288 --dup-per 0.5 > type2_runs/19_50_0.5.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 524288 --dup-per 0.7 > type2_runs/19_50_0.7.log
python ../main_int.py --psi-type 2 --num-clients 50 --num-ele 524288 --dup-per 0.9 > type2_runs/19_50_0.9.log

end_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
echo $end_date_time;
