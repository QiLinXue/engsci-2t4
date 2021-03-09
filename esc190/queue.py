queue = []
        
# Add in entries
queue.append('a')
queue.append('b')
queue.append('c')

# The first entry added was 'a' so the first entry that comes out will be 'a'
out = queue.pop(0)
print(out) # 'a'