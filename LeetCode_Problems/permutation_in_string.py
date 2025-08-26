"""
Description: Given s1 and s2, return True if any permutation of s1 is a substring of s2.

Equivalent: is there a window of length len(s1) in s2 that has the same character frequencies as s1

I/P: s1 = ab, s2 = eidbaooo
O/P: True 
I/P: s1 = ab, s2 = eidboaooo
O/P: False 

Pseudocode:
if len(sq) > len(s2):return False 
build freq_s1 
build freq_window for first m chars of s2 
if freq_s1 == freq_window: return True 
slide window across s2:
    remove left char, add right char 
    if freq_window == freq_s1: return True 
return False 

"""

# Simple & Clear (uses collections.Counter)
from collections import Counter 

def checkInclusion_counter(s1: str, s2: str) -> bool:
    m, n = len(s1), len(s2) 
    if m > n:
        return False 
    
    c1 = Counter(s1) 
    window = Counter(s2[:m])
    if c1 == window:
        return True 
    
    for i in range(m,n):
        left_char = s2[i - m]
        # decrement left_char 
        if window[left_char] == 1:
            del window[left_char]
        else:
            window[left_char] -= 1 
        # add right_char 
        window[s2[i]] += 1
        if window == c1:
            return True 
    
    return False 

# Optimized Array (assumes lowercase a-z) 
def checkInclusion_array_opt(s1: str, s2:str)->bool:
    m,n = len(s1), len(s2)
    if m > n: return False 
    # frequency arrays for 'a'...'z'
    cnt1 = [0] * 26 
    cnt2 = [0] * 26 
    for ch in s1:
        cnt1[ord(ch) - 97] += 1

    for ch in s2[:m]:
        cnt2[ord(ch) - 97] += 1 

    if cnt1 == cnt2:
        return True 
    
    for i in range(m, n):
        right = ord(s2[i]) - 97
        left = ord(s2[i-m]) - 97
        cnt2[right] += 1 
        cnt2[left] -= 1
        if cnt1 == cnt2:
            return True 
        
    return False


if __name__== '__main__':
    tests = [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("adc", "dcda", True),
        ("hello", "ooolleoooleh", False),
        ("", "", True),
        ("a", "", False),
        ("xyz", "afdgzyxksldfm", True)
    ]

    for s1, s2, expected in tests:
        a = checkInclusion_counter(s1, s2) 
        b = None 
        if all('a'<= c <= 'z' for c in s1 + s2):
            b = checkInclusion_array_opt(s1, s2)
        print(f"s1={s1!r}, s2={s2!r}, expected={expected}, counter={a}, array={b}")
