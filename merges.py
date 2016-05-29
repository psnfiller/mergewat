import doctest
import sys

def minor(stack, size):
  return [size] + stack

def smallest_merge(stack, max_stack):
  if len(stack) <= max_stack:
    return stack, 0
  smallest = sys.maxint
  merge_point = -1
  for i in xrange(len(stack) - 1):
    v = stack[i] + stack[i+1]
    if v <= smallest:
      smallest = v
      merge_point = i
  return stack[:merge_point] + [smallest] + stack[merge_point+2:], smallest


def merge(stack, max_stack):
  """
  >>> merge([1,1], 5)
  ([1, 1], 0)
  >>> merge([1,1,1], 5)
  ([3], 3)
  >>> merge([1,1,2], 5)
  ([1, 1, 2], 0)
  >>> merge([1,1,1,1,1,1], 5)
  ([6], 6)
  >>> merge([100, 100, 300, 700, 1500, 3100], 5)
  ([100, 100, 300, 700, 4600], 4600)
  """
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
    assert merge_size == 0
    return cap_stack(stack, max_stack)
  items_below_merge_point = len(stack) - merge_point
  end_merge_size = 0
  diff = max_stack - items_below_merge_point - 1
  if diff > 0:
    merge_point += diff
  #if (items_below_merge_point + 1) > max_stack:
  #  end = max_stack - 2
  #  for i in xrange(max_stack, len(stack)):
  #    end_merge_size += stack[i]
  #  output = [merge_size] + stack[merge_point+1:end] + [end_merge_size]
  #else:
  merge_size = sum(stack[:merge_point])
  output = [merge_size] + stack[merge_point+1:]
  assert sum(stack) == sum(output), output
  assert len(output) <= max_stack
  return output, merge_size + end_merge_size

def cap_stack(stack, size):
  """
  >>> cap_stack([1,1,1,1], 2)
  ([1, 3], 3)
  >>> cap_stack([1,1,1,1], 5)
  ([1, 1, 1, 1], 0)
  """

  if len(stack) <= size:
    return stack, 0
  merge_size = 0
  for i in xrange(size-1, len(stack)):
    merge_size += stack[i]
  return stack[:size-1] + [merge_size], merge_size



def run(total, minor_size, max_stack, merge):
  stack = []
  tally = 0
  stack_tally= 0.0
  for i in xrange(total / minor_size):
    stack = minor(stack, minor_size)
    stack, s = merge(stack, max_stack)
    tally += s
    stack_tally += len(stack)
  print minor_size, max_stack, float(tally) / total, stack_tally/i


def main():
  stack = []
  tally = 0
  total = 1000* 1000
  for minor_size in (2048,1024,512,256,128,100, 10, 1):
    #for max_stack in (1,2,3,5,8,9,10,11,12,13,14,15,16,32):
    for max_stack in (1,2,3,5,8,10,12,14,16,32):
      avg_stack = run(total, minor_size, max_stack, smallest_merge)
  print minor_size, max_stack, float(tally) / total, stack_tally/i



#if __name__ == "__main__":
#  doctest.testmod()

if __name__ == "__main__":
  main()
