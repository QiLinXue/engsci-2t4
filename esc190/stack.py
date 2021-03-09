stack = []

# Add in entries
stack.append('a')
stack.append('b')
stack.append('c')

# The last entry added was 'c' so the first entry that comes out will be 'c'
out = stack.pop()
print(out) # 'c'