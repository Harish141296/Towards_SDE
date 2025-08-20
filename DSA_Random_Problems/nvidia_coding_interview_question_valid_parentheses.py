"""
Description: we have set of different types of brackets and we have 3 rules. 
1. opening of any brackets should be closed by the same bracket 
2. open brackets must be closed in the correct order.
3. every close bracket has a corresponding open bracket of the same type.

I/P: s = "{}[(])"
O/P: Not a Valid Parentheses
Exp: Brackets were not closed in the right order 

I/P: s = "{}[]("
O/P: Not a Valid Parentheses
Exp: closing parentheses was not found.

I/P: s = "{}[]"
O/P: Valid Parentheses
Exp: Brackets were closed in the right order 


"""

class solution:
    def isValid(self, s: str) -> bool:
        hashmap = {')':'(','}':'{',']':'['}
        stk = [] 
        for c in s:
            if c not in hashmap:
                stk.append(c) 
            else:
                if not stk:
                    return False 
                else:
                    popped = stk.pop()
                    if popped != hashmap[c]:
                        return False 
        return not stk 


if __name__ == '__main__':
    s = "{}[(])"
    sol = solution()
    if sol.isValid(s):
        print("Valid parentheses")
    else:
        print("not a valid parentheses")