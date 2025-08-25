"""
Description: Given a string s, find the length of Longest Substring without repeating characters.
I/P: S = "abcabcbb"
O/P: 3

I/P: S = "bbbbbb"
O/P: 1 

Formulae: W = (R - L) + 1 
"""


def longest_substring_debug(s: str) -> int: 
    last = {} 
    L = 0 
    best = 0 
    for r, ch in enumerate(s):
        if ch in last:
            # jump L only forward; never backward
            L = max(L, last[ch] + 1)
        last[ch] = r 
        best = max(best, r - L + 1)
        print(f"L = {L}, R= {r}, ch={ch!r}, curr_len = {r-L + 1}, best = {best}")
    return best 


assert longest_substring_debug("") == 0
assert longest_substring_debug("a") == 1 
assert longest_substring_debug("bbbbbbbbbbbb") == 1
assert longest_substring_debug("abcabcbb") == 3 
assert longest_substring_debug("pwwkew") == 3  # wke
assert longest_substring_debug("dvdf") == 3 # vdf
assert longest_substring_debug("harish") == 5 
