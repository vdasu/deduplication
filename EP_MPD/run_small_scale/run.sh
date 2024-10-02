mkdir -p type1_runs
mkdir -p type2_runs

start_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
echo $start_date_time;

# Type 1 runs
# Effect of Client Count. Fix dataset size to 2^15, duplication percentage to 30% and vary client count in [5,10,15,20,25]
python ../main_int.py --psi-type 1 --num-clients 5 --num-ele 32768 --dup-per 0.3 > type1_runs/15_5_0.3.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32768 --dup-per 0.3 > type1_runs/15_10_0.3.log
python ../main_int.py --psi-type 1 --num-clients 15 --num-ele 32768 --dup-per 0.3 > type1_runs/15_15_0.3.log
python ../main_int.py --psi-type 1 --num-clients 20 --num-ele 32768 --dup-per 0.3 > type1_runs/15_20_0.3.log
python ../main_int.py --psi-type 1 --num-clients 25 --num-ele 32768 --dup-per 0.3 > type1_runs/15_25_0.3.log

# Effect of Dataset size. Fix client to count to 10, duplication percentage to 30% and vary dataset size in [2^5, 2^7, 2^10, 2^13, 2^15]
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32 --dup-per 0.3 > type1_runs/5_10_0.3.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 128 --dup-per 0.3 > type1_runs/7_10_0.3.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 1024 --dup-per 0.3 > type1_runs/10_10_0.3.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 8192 --dup-per 0.3 > type1_runs/13_10_0.3.log

# Effect of duplication percentage. Fix client count to 10, datasize size to 2^15, and vary duplication percentage in [10%, 30%, 50%, 70%, 90%]
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32768 --dup-per 0.1 > type1_runs/15_10_0.1.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32768 --dup-per 0.5 > type1_runs/15_10_0.5.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32768 --dup-per 0.7 > type1_runs/15_10_0.7.log
python ../main_int.py --psi-type 1 --num-clients 10 --num-ele 32768 --dup-per 0.9 > type1_runs/15_10_0.9.log


# Type 2 runs
# Effect of Client Count. Fix dataset size to 2^15, duplication percentage to 30% and vary client count in [5,10,15,20,25]
python ../main_int.py --psi-type 2 --num-clients 5 --num-ele 32768 --dup-per 0.3 > type2_runs/15_5_0.3.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32768 --dup-per 0.3 > type2_runs/15_10_0.3.log
python ../main_int.py --psi-type 2 --num-clients 15 --num-ele 32768 --dup-per 0.3 > type2_runs/15_15_0.3.log
python ../main_int.py --psi-type 2 --num-clients 20 --num-ele 32768 --dup-per 0.3 > type2_runs/15_20_0.3.log
python ../main_int.py --psi-type 2 --num-clients 25 --num-ele 32768 --dup-per 0.3 > type2_runs/15_25_0.3.log

# Effect of Dataset size. Fix client to count to 10, duplication percentage to 30% and vary dataset size in [2^5, 2^7, 2^10, 2^13, 2^15]
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32 --dup-per 0.3 > type2_runs/5_10_0.3.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 128 --dup-per 0.3 > type2_runs/7_10_0.3.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 1024 --dup-per 0.3 > type2_runs/10_10_0.3.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 8192 --dup-per 0.3 > type2_runs/13_10_0.3.log

# Effect of duplication percentage. Fix client count to 10, datasize size to 2^15, and vary duplication percentage in [10%, 30%, 50%, 70%, 90%]
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32768 --dup-per 0.1 > type2_runs/15_10_0.1.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32768 --dup-per 0.5 > type2_runs/15_10_0.5.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32768 --dup-per 0.7 > type2_runs/15_10_0.7.log
python ../main_int.py --psi-type 2 --num-clients 10 --num-ele 32768 --dup-per 0.9 > type2_runs/15_10_0.9.log

end_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
echo $end_date_time;
