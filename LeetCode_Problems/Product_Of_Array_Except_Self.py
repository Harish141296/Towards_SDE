"""
Description: Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i]
  The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer 
  You must write an algorithm that runs in O(n) time and without using the division operations 

I/P: nums = [1, 2, 3, 4]
O/P: [24, 12, 8, 6]

I/P: nums = [-1, 1, 0, -3, 3]
O/P: [0, 0, 9, 0, 0]

"""

class Solution: 
    def productofarrayexceptself(self, nums: list[int])-> list[int]:
        res = [1] * (len(nums))
        prefix = 1 
        for i in range(len(nums)):
            res[i] = prefix 
            prefix *= nums[i] 
        postfix = 1 
        for i in range(len(nums) -1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        return res 
    
sol = Solution()
ip = [1, 2, 3, 4]
print(sol.productofarrayexceptself(ip))


ip = [-1, 1, 0, -3, 3]
print(sol.productofarrayexceptself(ip))
