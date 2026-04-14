'''
3. Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without duplicate characters.
Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

'''

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        char_set = set()
        left_index = 0
        max_len = 0

        for right_index in range(len(s)):
            while s[right_index] in char_set:
                char_set.remove(s[left_index])
                left_index += 1

            char_set.add(s[right_index])

            max_len = max(max_len, right_index-left_index+1)
        return max_len

s = "abcabcbb"
sol = Solution()
result = sol.lengthOfLongestSubstring(s)
print(result)
