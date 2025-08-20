"""
Description: Given a string s, find the length of Longest Substring without repeating characters.
I/P: S = "abcabcbb"
O/P: 3

I/P: S = "bbbbbb"
O/P: 1 

Formulae: W = (R - L) + 1 
"""
class Solution:
    def __init__(self, s:str):
        self.s = s 

    def lengthoflongestsubstring(self):
        l = 0 
        longest = 0 
        sett = set() 
        n = len(self.s)

        for r in range(n):
            while self.s[r] in sett:
                sett.remove(s[l])
                l += 1
            w = (r - l) + 1 
            longest = max(longest, w)
            sett.add(s[r])
        return longest 

if __name__ == '__main__':
    s = "abcabcbb"
    sol = Solution(s)
    longest_count = sol.lengthoflongestsubstring()
    print(f"The Longest substring is: {longest_count}")
