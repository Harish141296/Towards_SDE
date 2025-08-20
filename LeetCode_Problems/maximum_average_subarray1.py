"""
Description: You are given an integer array nums consisting of n elements, and an integer k.
Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10^ -5 will be accepted.

I/P: nums = [1, 12, -5, -6, 50, 3], k = 4
O/P: 3
Exp: Maximum average is (12 - 5 - 6 + 50)/ 4 = 12.75
"""

class Solution:
    def __init__(self, nums:list[int], k:int):
        self.nums = nums 
        self.k = k 
    def findMaxAverage(self):
        n = len(self.nums)
        cur_sum = 0 
        # Building up the window
        for i in range(self.k):
            cur_sum += self.nums[i]
        max_avg = cur_sum / self.k
        # processing the rest by moving the window 
        for i in range(self.k, n):
            cur_sum += self.nums[i]
            cur_sum -= self.nums[i-k]
            avg = cur_sum / self.k
            max_avg = max(max_avg, avg)
        
        return max_avg

if __name__ == '__main__':
    nums = [1, 12, -5, -6, 50, 3]
    k = 4
    sol = Solution(nums, k)
    avg = sol.findMaxAverage()
    print(f"The Maximum Average of given array is: {avg}")