"""
Description: Given an Integer array nums, find the contiguous subarray (containing atleast one number) which has the largest sum and return its sum.
I/P: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
O/P: 6

"""

class Solution: 
    def maxSubArray(self, nums: list[int])->int:
        maxSub = nums[0]
        curSum = 0
        for n in nums:
            if curSum < 0 :
                curSum = 0
            curSum += n 
            maxSub = max(maxSub, curSum)
        return maxSub 


if __name__ == '__main__':
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    sol = Solution()
    print(sol.maxSubArray(nums))
