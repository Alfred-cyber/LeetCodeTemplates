'''
643. Maximum Average Subarray I

You are given an integer array nums consisting of n elements, and an integer k.
Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value.
Any answer with a calculation error less than 10-5 will be accepted.

 

Example 1:

Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
Example 2:

Input: nums = [5], k = 1
Output: 5.00000

'''
nums = [1,12,-5,-6,50,3]
k = 4

class Solution(object):
    def findMaxAverage(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: float
        """
        if len(nums) < k:
            return 0
        
        curr_wind_av = sum(nums[:k])
        best_av_seen = curr_wind_av

        for r in range(k, len(nums)):
            element_entering = nums[r]
            element_leaving = nums[r-k]

            curr_wind_av += element_entering
            curr_wind_av -= element_leaving
            best_av_seen = max(best_av_seen, curr_wind_av)

        return best_av_seen/float(k)

res = Solution().findMaxAverage(nums,k)
print(res)
            
        