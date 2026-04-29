'''
Given an integer array nums sorted in non-decreasing order, 
return an array of the squares of each number sorted in non-decreasing order.

Example 1:

Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].
Example 2:

Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]

'''

class Solution(object):
    def sortedSquares(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        length = len(nums)

        sqr_sorted = [0]*length

        left_index = 0
        right_index = length - 1
        pos = length - 1

        while left_index <= right_index:
            left_val = nums[left_index]
            right_val = nums[right_index]

            left_sqr = left_val*left_val
            right_sqr = right_val*right_val

            #Put the bigger squre at the current pos
            if left_sqr > right_sqr:
                sqr_sorted[pos] = left_sqr
                left_index += 1
            else:
                sqr_sorted[pos] = right_sqr
                right_index -= 1
            pos -= 1
        return sqr_sorted
    
nums = [-4, -1, 0, 3, 10]
sol = Solution()
print(sol.sortedSquares(nums))

        
