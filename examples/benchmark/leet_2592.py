def maximizeGreatness(nums):
    nums.sort()
    n=len(nums)
    ans=0
    rem=0 #Numbers greater than the current number
    curem=0 #Numbers equal to the current number
    comp= nums[n-1] #The last greatest number we have encountered so far
    for i in range(n-2,-1,-1):
        if(nums[i]<comp): #[3,4] we are checking 3 here
            comp=nums[i] #found a new guy
            rem+=curem #include the number of 3s in our numbers greater than nums[i] counter
            curem=0 #Reset the count of numbers same as nums[i]
            ans+=1
        elif(nums[i]==nums[i+1]): 
            if(rem>0): #if there is a spare number above, incrememnt sum 
                rem-=1
                ans+=1
            curem+=1 #this number cannot be paired, but we can use it later
    return ans
        
import time
start_time = time.perf_counter()
for _ in range(100000):
    maximizeGreatness(list(map(int, '14213151565456346')))
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")