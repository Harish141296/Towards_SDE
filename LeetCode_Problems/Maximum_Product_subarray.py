"""
Description: Given an Integer array nums, find the contiguous subarray within an array (containing atleast one number) which has the largest product.
I/P: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
O/P: 6

"""

class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        res = max(nums)
        curMin, curMax = 1, 1 

        for n in nums:
            if n == 0:
                curMin, curMax = 1, 1 
                continue 
            temp = curMax * n 
            curMax = max (n * curMax, n* curMin, n)
            curMin = min(temp, n * curMin, n)
            res = max(res, curMax)
        return res 
    

if __name__ == '__main__':
    nums = [2, 3, -2, 4]
    sol = Solution()
    print(sol.maxProduct(nums))
