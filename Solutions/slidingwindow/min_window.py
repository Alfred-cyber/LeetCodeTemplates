'''
76. Minimum Window Substring

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

 

Example 1:

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
Example 2:

Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.
Example 3:

Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.
 

Constraints:

m == s.length
n == t.length
1 <= m, n <= 105
s and t consist of uppercase and lowercase English letters.
 

Follow up: Could you find an algorithm that runs in O(m + n) time?
'''

class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        from collections import Counter

        if not s or not t:
            return ""
        need = Counter(t)
        missing = len(t)
        left = start = end = 0

        for right in range(len(s)):
            #If current character is needed, reduce the missing count
            if need[s[right]] > 0:
                missing -= 1
            need[s[right]] -= 1

            while missing == 0:
                if end == 0 or right-left+1 < end-start:
                    start = left
                    end = right+1

                #shrink from left
                need[s[left]] += 1
                if need[s[left]] > 0:
                    missing += 1
                left += 1
        return s[start:end]

s = "ADOBECODEBANC"
t = "ABC"
sol = Solution()
result = sol.minWindow(s,t)
print(result)