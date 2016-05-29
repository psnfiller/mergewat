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

  >>> merge([1,1,1])
  ([3], 3, False)

  """
  merge_point = -1
  merge_size = 0
  depth = False
  if len(stack) > 5:
    depth = True
    merge_point = 5
    for i in xrange(5):
      merge_size += stack[i]
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
  return [merge_size] + stack[merge_point+1:], merge_size, depth


def run(total, minor_size):
  stack = []
  tally = 0
  for i in xrange(total / minor_size):
    stack = minor(stack, minor_size)
    #print stack
    stack,s, depth  = merge(stack)
    tally += s
    print "merge", stack,  s, tally, depth
  return tally

def main():
  stack = []
  tally = 0
  total = 1000
  #minor_size = 100
  #print minor_size, run(total, minor_size)
  #minor_size = 10
  #print minor_size, run(total, minor_size)
  minor_size = 1
  print minor_size, run(total, minor_size)



if __name__ == "__main__":
  doctest.testmod()

#if __name__ == "__main__":
#  main()
