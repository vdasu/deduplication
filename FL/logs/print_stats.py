from collections import defaultdict
import os


clients = [0,1,2,3,4,5,6,7,8,9]
rnds = [0,1,2,3,4]
folders = ["nodup", "10", "20", "30"]
datasets = ["haiku", "haiku_large", "imdb", "jokes", "jokes_large", "plays", 
            "poetry", "rotten", "rotten_large", "sonnets", "sonnets_large"]


for dataset in datasets:

    times = []
    ppls = []

    for folder in folders:

        exec_time = defaultdict(list)
        agg_time = defaultdict(list)

        files = os.listdir(f"./{dataset}/{folder}")
    
        for f in files:
            if f".o" in f:
                file = f
                break
        
        file = f"./{dataset}/{folder}/" + file 

        with open(file, "r") as f:
            lines = f.readlines()

        for rnd in rnds:
            for client in clients:
                for line in lines:
                    if f"Client {client} round {rnd} took" in line:
                        exec_time[rnd].append(float(line.split()[-2]))
            for line in lines:
                if "Aggregation took" in line and f"round {rnd}" in line:
                    agg_time[rnd].append(float(line.split()[2]))

        tot_time = 0

        # Only compute GPU training time. Aggregation time is always the same
        for rnd in rnds:
            tot_time += sum(exec_time[rnd])

        times.append(round(tot_time / 60, 2))
        ppls.append(float(lines[-1].split(": ")[1]))

    print("Dataset: ", dataset)
    
    print("Time: ")

    print("Nodup: ", round(times[0], 2))
    for folder, time in zip(folders[1:], times[1:]):
        print(folder,"Time: ", round(time, 2), ", IR: ", round((time - times[0]) / time * 100, 2))

    print("\nPerplexity: ")
    print("Nodup: ", round(ppls[0], 2))
    for folder, ppl in zip(folders[1:], ppls[1:]):
        if ppl > ppls[0]:
            print(folder, "Perplexity: ", round(ppl, 2), ", IR: ", round((ppl - ppls[0]) / ppl * 100, 2))
        else:
            print(folder, "Perplexity: ", round(ppl, 2), ", IR: N/A")
    
    print("\n\n")
