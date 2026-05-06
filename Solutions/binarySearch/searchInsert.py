class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid_index = left + (right - left)//2
            mid_val = nums[mid_index]

            if mid_val == target:
                return mid_index
            elif mid_val < target:
                left = mid_index + 1
            else:
                right = mid_index - 1

        return left

