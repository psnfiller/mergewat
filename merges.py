import doctest
import copy
import sys

def minor(stack, size):
  return [size] + stack

def smallest_merge(stack):
  if len(stack) <= 5:
    return stack, 0
  smallest = sys.maxint
  merge_point = -1
  for i in xrange(len(stack) - 1):
    v = stack[i] + stack[i+1]
    if v <= smallest:
      smallest = v
      merge_point = copy.copy(i)
  return stack[:merge_point] + [smallest] + stack[merge_point+2:], smallest

def merge(stack):
  """Merges.

  >>> merge([1,1])
  ([1, 1], 0, 0, False)
  >>> merge([1,1,1])
  ([1, 1, 1], 0, 0, False)
  >>> merge([1,1,2])
  ([1, 1, 2], 0, 0, False)
  >>> merge([1,1,1,1,1,1])
  ([1, 1, 4], 4, 2, True)

  """
  max_depth = 5
  merge_point = sys.maxint
  depth = False
  if len(stack) > 5:
    depth = True
    merge_point = 5

  size = 0
  for i in xrange(len(stack)):
    if stack[i] < size:
      if merge_point > i:
        merge_point = i
    size += stack[i]

  if merge_point == sys.maxint or merge_point +1  == len(stack):
    return stack, 0, 0, False

  merge_size = 0
  for i in xrange(merge_point, len(stack)):
    merge_size += stack[i]
  output = stack[:merge_point] + [merge_size]
  assert len(output) < max_depth
  assert sum(stack) == sum(output), output
  return output, merge_size, merge_point, depth

def merge4(stack, max_stack):
  merge_point = -1
  merge_size = 0
  size = 0
  for i in xrange(len(stack)):
    if stack[i] < size:
      if merge_point < i:
        merge_point = i
        merge_size = size + stack[i]
    size += stack[i]
  if merge_point == -1:
    return stack, 0
  below_merge_point = len(stack[merge_point+1:])
  end_merge_size = 0
  if (below_merge_point + 1) > max_stack:
    end = merge_point+1 + (max_stack - 2)
    for i in xrange(end, len(stack)):
      end_merge_size += stack[i]
    output = [merge_size] + stack[merge_point+1:end] + [end_merge_size]
  else:
    output = [merge_size] + stack[merge_point+1:]
  assert sum(stack) == sum(output), output
  return output, merge_size + end_merge_size
def merge3(stack):
  merge_point = -1
  merge_size = 0
  size = 0
  for i in xrange(len(stack)):
    if stack[i] < size:
      if merge_point < i:
        merge_point = i
        merge_size = size + stack[i]
    size += stack[i]
  if merge_point == -1:
    return stack, 0
  output = [merge_size] + stack[merge_point+1:]
  assert sum(stack) == sum(output), output
  return output, merge_size

def merge2(stack):
  max_depth = 5
  merge_point = -1
  merge_size = 0
  depth = False
  if len(stack) > 5:
    depth = True
    merge_point = 5
    for i in xrange(5, len(stack)):
      merge_size += stack[i]
    output = stack[:merge_point] + [merge_size]
    print output
    assert sum(stack) == sum(output), output
  smallest = sys.maxint
  size = 0
  for i in xrange(len(stack)):
    if stack[i] < size:
      if merge_point < i:
        merge_point = i
        merge_size = size + stack[i]
    size += stack[i]
  if merge_point == -1:
    return stack, 0, False
  output = [merge_size] + stack[merge_point:]
  assert len(output) < max_depth
  assert sum(stack) == sum(output), output
  return output, merge_size, depth

def cap_stack(stack, size):
  """
  >>> cap_stack([1,1,1,1], 2)
  ([1, 3], 3)

  """

  merge_size = 0
  for i in xrange(size-1, len(stack)):
    merge_size += stack[i]
  return stack[:size-1] + [merge_size], merge_size



def run(total, minor_size):
  stack = []
  tally = 0
  max_stack = 5
  for i in xrange(total / minor_size):
    stack = minor(stack, minor_size)
    stack,s = merge4(stack)
    tally += s
    if len(stack) > max_stack:
      assert False
      #stack, s = cap_stack(stack, max_stack)
      #tally += s
      pass
    #print "merge", stack,  s, tally
  print minor_size, tally, float(tally) / total, max_stack
  return tally

def main():
  stack = []
  tally = 0
  total = 10* 1000
  minor_size = 100
  for minor_size in (100, 10, 1):
    run(total, minor_size)



#if __name__ == "__main__":
#  doctest.testmod()

if __name__ == "__main__":
  main()
