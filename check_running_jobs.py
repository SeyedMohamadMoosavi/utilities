#! /usr/bin/env python


from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np 
import sys
import os
import subprocess

    
def get_status(jobs):
    running=0
    pending=0
    for job in jobs:
        if job.strip().split()[4]=="R":
            running+=1
        elif job.strip().split()[4]=="PD":
            pending+=1
    print("\n===================================\n")
    print("Submitted jobs to the cluster:  %i"%len(jobs))
    print("Running jobs: %i"%running)
    print("Pending jobs: %i"%pending)
    print("\n===================================\n")

def get_job_ids(jobs):
    run_ids = []
    pd_ids = []
    for job in jobs:
        if job.strip().split()[4]=="R":
            run_ids.append(int(job.strip().split()[0])) 
        elif job.strip().split()[4]=="PD":
            pd_ids.append(int(job.strip().split()[0]))

    return run_ids,pd_ids



username = "moosavi"
group_name = "lsmo"
max_jobs = 4950

p=subprocess.Popen(["sshare","-a"],
       stderr=subprocess.PIPE,stdout=subprocess.PIPE)
(stdout , stderr)= p.communicate()
share_status=stdout.decode("utf-8").split("\n")
share_status = [l for l in share_status if group_name in l]
group_share = float(share_status[0].strip().split()[2])
group_usage = float(share_status[0].strip().split()[4])

#print("Group share coefficient: %f"%group_share)
# print("Group usage coefficient: %f"%group_usage)
# if group_usage/group_share < 0.9:
#     print("Safe to submit jobs")
# else:
#     print("\n\nThink twice!!\n group usage is high and you might want to wait")
#     cond = input("Do you want to submit more jobs?[y/n] ")
#     if cond.lower() == "n":
#         sys.exit()
# 
# 
p=subprocess.Popen(["squeue","-u",username],
       stderr=subprocess.PIPE,stdout=subprocess.PIPE)
(submitted , stderr)= p.communicate()
current_jobs=submitted.decode("utf-8").split("\n")
current_jobs = [n for n in current_jobs[1:] if not n==""]

# get_status(current_jobs)

run_ids,pd_ids = get_job_ids(current_jobs)

p=subprocess.Popen(["find",sys.argv[1],"-name","slurm-*"],
       stderr=subprocess.PIPE,stdout=subprocess.PIPE)
(directories , stderr)= p.communicate()
running_jobs =directories.decode("utf-8").split("\n")
running_jobs = [int(n.split("-")[-1].strip(".out")) for n in running_jobs if not n==""]

rj = 0
for job in running_jobs:
    if job in run_ids:
        print(job)
        rj +=1

print("\n\n%i jobs are running, no idea about pending jobs!\n\n"%rj)









# with open("waiting_list","r") as fi:
#     waiting_jobs = [l.strip() for l in fi.readlines()]
# 
# with open("submitted_list","r") as fi:
#     submitted_jobs = [l.strip() for l in fi.readlines()]
# 
# q_jobs = len(current_jobs)
# s_jobs = min(max_jobs - q_jobs,len(waiting_jobs))
# print("submitting %i jobs.."%s_jobs)
# with open("submitted_list","a") as fo:
#     for i in range(s_jobs):
#         cjob = waiting_jobs[i]
#         job_dir = "/".join(cjob.split("/")[:-1])
#         job_name = cjob.split("/")[-1]
#         p=subprocess.Popen(["sbatch",job_name],
#                        stderr=subprocess.PIPE,stdout=subprocess.PIPE,cwd=job_dir)
#         (stdout , stderr)= p.communicate()
#         fo.write("%s\n"%cjob)
#         
# 
# 
# with open("waiting_list","w") as fo:
#     for j in waiting_jobs[s_jobs:]:
#         fo.write("%s\n"%j)
# 
