import doctest
import sys
import numpy
import operator

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

# TODO(psn): this is really slow.
def smallest_n_merge(stack, max_stack, n):
  """
  >>> smallest_n_merge([1,1,1,1,1], 3, 3)
  ([1, 1, 3], 3)
  """
  if len(stack) <= max_stack:
    return stack, 0
  smallest = sys.maxint
  merge_point = -1
  for i in xrange(len(stack) - n+1):
    v = sum(stack[i:i+n])
    if v <= smallest:
      smallest = v
      merge_point = i
  return stack[:merge_point] + [smallest] + stack[merge_point+n:], smallest

def smallest_4_merge(stack, max_stack):
  return smallest_n_merge(stack, max_stack, 4)


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
  >>> merge([2048, 2048, 2048], 2)
  ([6144], 6144)
  """
  merge_point = -1
  size = 0
  for i in xrange(len(stack)):
    if stack[i] < size:
      if merge_point < i:
        merge_point = i
    size += stack[i]
  mp = merge_point
  items_below_merge_point = len(stack) - merge_point
  if merge_point == -1 or items_below_merge_point == 0 :
    return cap_stack(stack, max_stack)
  diff = (items_below_merge_point +1 ) - max_stack
  if items_below_merge_point + 1 > max_stack:
    #if merge_point + diff > max_stack:
    #  merge_point = len(stack) - max_stack -1
    #else:


    merge_point += diff
  merge_size = sum(stack[:merge_point+1])
  output = [merge_size] + stack[merge_point+1:]
  #print stack, output, merge_point, mp, diff
  assert sum(stack) == sum(output), "merge(%r, %r) %r %r" % (stack, max_stack, output, merge_point)
  assert len(output) <= max_stack, "merge(%r, %r) %r %r %r" % (stack, max_stack, output, merge_point, mp)
  return output, merge_size

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
  stack_tally = []
  for i in xrange(total / minor_size):
    stack = minor(stack, minor_size)
    stack, s = merge(stack, max_stack)
    tally += s
    stack_tally.append(len(stack))
  print minor_size, max_stack, float(tally) / total, sum(stack_tally)/float(i), numpy.std(stack_tally)
  return float(tally) / total, sum(stack_tally)/float(i), numpy.std(stack_tally)


def humanize(i):
  """
  >>> humanize(123)
  '123'
  >>> humanize(1234)
  '1.2k'
  """
  suffixes = ['', 'k', 'M', 'B']
  s = 0
  i = float(i)
  while i > 1000:
    i/=1000
    s+=1
  if s == 0:
    return "%d" % int(i)
  return "%3.1f%s" % (i, suffixes[s])

def main():
  stack = []
  tally = 0
  total = 1000 * 1000
  smallest = {}
  #for minor_size in (2048,1024,512,256,128,64,32,16,8,4,2):
  for minor_size in (128,):
    for max_stack in (1,2,3,5,8,10,12,14,16,32):
      v = run(total, minor_size, max_stack, smallest_4_merge)
      k = '%d-%d' % (minor_size, max_stack)
      #print minor_size, max_stack, v
      smallest[k] = v

  return
  n = set()
  normal = {}
  for minor_size in (2048,1024,512,256,128,64,32,16,8,4,2):
    for max_stack in (1,2,3,5,8,10,12,14,16,32):
      v = run(total, minor_size, max_stack, merge)
      k = '%d-%d' % (minor_size, max_stack)
      normal[k] = v
      n.add((v[0]* v[1], v[0], v[1], minor_size, max_stack))
  for minor_size in (2048,1024,512,256,128,64,32,16,8,4,2):
    for max_stack in (1,2,3,5,8,10,12,14,16,32):
      k = '%d-%d' % (minor_size, max_stack)
      print minor_size, max_stack,
      avg_merge, avg_stack, stddev_stack = smallest[k]
      print "%s %s" % (humanize(avg_merge), humanize(avg_stack)),
      avg_merge, avg_stack, stddev_stack = normal[k]
      print "%s %s" % (humanize(avg_merge), humanize(avg_stack))
  for k in sorted(n, key=operator.itemgetter(0,1))[:60]:
    print k






#if __name__ == "__main__":
#  doctest.testmod()

if __name__ == "__main__":
  main()
