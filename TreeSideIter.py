from math import inf

l = 'left'
r = 'right'
d = 'data'
s = 'starting'
e = 'ending'
LEFT = "LEFT"
RIGHT = "RIGHT"
evalEnumSet = set([LEFT, RIGHT])

def getRightTree():

  tree = {
      d: {
        s: 0,
        e: 7
        },
      r: {
        l: 0,
        r: 0,
        d: {
          s: 2,
          e: 4
        }
      },
      l: {
        l: 0,
        d: {
          s: 1,
          e: 9
        },
        r: {
          d: {
            s: 3,
            e: 6
            },
          r: {
            d: {
              s: 5,
              e: 3
            },
            l:0,
              r:{
                d: {
                  s: 7,
                  e: 1
                  },
                l: 0,
                r: 0
              }
          },
          l: {
            d: {
              s: 4,
              e: 8
            },
            l: 0,
            r:{
              d: {
                s: 6,
                e: 5,
              },
              l: 0,
              r:{
                d: {
                  s: 8,
                  e: 2
                },
                l: 0,
                r: {
                  d: {
                    s: 9,
                    e: 0
                  },
                  l: 0,
                  r: 0
                }
              }
            }
          },
        }
      },
    }
  return tree

def getLeftTree():

  tree = {
      d: {
        s: 0,
        e: 4
        },
      r: {
        l: 0,
        r: 0,
        d: {
          s: 2,
          e: 7
        }
      },
      l: {
        l: 0,
        d: {
          s: 1,
          e: 1
        },
        r: {
          d: {
            s: 3,
            e: 3
            },
          r: {
            d: {
              s: 5,
              e: 6
            },
            l:0,
              r:{
                d: {
                  s: 7,
                  e: 9
                  },
                l: 0,
                r: 0
              }
          },
          l: {
            d: {
              s: 4,
              e: 0
            },
            l: 0,
            r:{
              d: {
                s: 6,
                e: 2,
              },
              l: 0,
              r:{
                d: {
                  s: 8,
                  e: 5
                },
                l: 0,
                r: {
                  d: {
                    s: 9,
                    e: 8
                  },
                  l: 0,
                  r: 0
                }
              }
            }
          },
        }
      },
    }
  return tree


def traverse_tree(tree, dir, _list,path=[], r_depth=0, l_depth=0, max_layers=0, min_layers=0):
  '''
  Recursively traverse down the tree
  (Depth First Search)
  args:
    tree: dict(dict(...))
          each node has
          left: 0 | dict
          right: 0 | dict
          data: dict
    _list: [{treeNode}, {treeNode}, ...]
    r_depth: times the right path was taken
    l_depth: times the left path was take
    max_layers: the highest layer number
    min_layer: the smallest layer number (may be negative)

  '''
  ###  branchless programming
  layer =((((r_depth - l_depth) >= (l_depth - r_depth)) * (r_depth - l_depth)) +
          (((l_depth - r_depth) > ( r_depth - l_depth)) * -1 * (l_depth - r_depth)))
  ### layer is the side - to - side value of where the node is in the tree
  node = {
    d: tree[d],
    'layer': layer,
    'depth': r_depth + l_depth,
    'path': path,
  }
  rt, lt = tree[r], tree[l]
  _list.append(node)
  max_l, min_l = max(layer, max_layers), min(layer, max_layers)

  def eval_right():
    # eval the right branches before the left branches
    r_max, l_max, r_min, l_min = -1 * inf, -1 * inf, inf, inf
    if(type(rt) == dict):
      _, r_max, r_min  = traverse_tree(rt, dir, _list, path + [r], r_depth+1, l_depth, max_l, min_l)
    if(type(lt) == dict):
      _, l_max, r_min = traverse_tree(lt, dir, _list, path + [l], r_depth, l_depth+1, max_l, min_l)
    return (_list, max(layer, max_layers, r_max, l_max), min(layer, min_layers, r_min, l_min))

  def eval_left():
    # eval the left branches before the right branches
    r_max, l_max, r_min, l_min = -1 * inf, -1 * inf, inf, inf
    if(type(lt) == dict):
      _, l_max, l_min = traverse_tree(lt, dir, _list, path + [l], r_depth, l_depth+1, max_l, min_l)
    if(type(rt) == dict):
      _, r_max, r_min  = traverse_tree(rt, dir, _list, path + [r], r_depth+1, l_depth, max_l, min_l)
    return (_list, max(layer, max_layers, r_max, l_max), min(layer, min_layers, r_min, l_min))

  if(dir is RIGHT):
    return eval_right()
  if(dir is LEFT):
    return eval_left()

  return (_list, max(layer, max_layers), min(layer, min_layers))

def getNodesFromLayer(tr, layer, _tree_spec, threshold_layer, dir):
  '''
  Recursively get layer and depth of node
  and puts the item in the _tree_spec list
  return _tree_spec
  '''
  new_tr = list()
  to_add = dict()
  for i in tr:
    if(i['layer'] == layer):
      # depth =i['depth']
      to_add[i['depth']] = i
    else:
      new_tr.append(i)
  while len(to_add.keys()) > 0:
    '''
    assumes each node has one branch (max depth case)
    arranges the tree based on depth of node
    deeper nodes are read first
    list is in reverse order
    '''
    i = max(list(to_add.keys()))
    _tree_spec.append(to_add[i])
    del to_add[i]

  if(dir is RIGHT):
    if(layer < threshold_layer):
      return _tree_spec
    newLayer = layer - 1
  if(dir is LEFT):
    if(layer > threshold_layer):
      return _tree_spec
    newLayer = layer + 1

  return getNodesFromLayer(new_tr, newLayer, _tree_spec, threshold_layer, dir)


def getTreeSpec(tree, evalEnum=RIGHT):
  """
  builds a treeSpec structure which represents a destructed tree.
  returns [{treeNode}, {treeNode}]

  given an asymmetric tree:
      n0
  n1 --^-- n2
  ^-- n3
  n4 --^-- n5
  ^-- n6    ^-- n7
        ^-- n8
            ^-- n9

  return tree evaluated from side:
  right -> left
  or
  left -> right

  right -> left example

      n7
  n9 --^-- n4
  ^-- n6
  n8 --^-- n3
  ^-- n5    ^-- n1
       ^-- n2
            ^-- n0


  left -> right example

      n4
  n1 --^-- n7
  ^-- n3
  n0 --^-- n6
  ^-- n2    ^-- n9
       ^-- n5
            ^-- n8
  """
  t, max_layers, min_layers = traverse_tree(tree, evalEnum, list())
  reversed = t[::-1]
  try:
    if(evalEnum is RIGHT):
      tree_spec = getNodesFromLayer(reversed, max_layers, list(), min_layers, evalEnum)
      if(len(reversed) != len(tree_spec)):
        raise ValueError('{r} != {ts} || Should be of equal lengths'.format(r=len(reversed), ts=len(tree_spec)))
    if(evalEnum is LEFT):
      tree_spec = getNodesFromLayer(reversed, min_layers, list(), max_layers, evalEnum)
      if(len(reversed) != len(tree_spec)):
        raise ValueError('{r} != {ts} || Should be of equal lengths'.format(r=len(reversed), ts=len(tree_spec)))
  except ValueError as err:
    print("Some Items got dropped or added in the getNodesFromLayer method")
    print(err)

  return tree_spec


def test_tree(tree_spec):
  # [{treeNode}, {treeNode}]
  hasErrored = False
  passed, total, = 0, 0
  try:
    if(len(tree_spec) == 0):
      raise AssertionError("ERROR: treeSpec cannot be empty")
    else:
      passed += 1
      total += 1
  except AssertionError as err:
    hasErrored = True
    total += 1
    print(err)

  try:
    for i in range(0, len(tree_spec)):
      item = tree_spec[i]
      if(item[d][e] != i):
        raise ValueError
    passed += 1
    total += 1
  except ValueError:
    hasErrored = True
    total += 1
    for i in tree_spec:
      print(i[d][s], i[d][e])
    print("invalid tree: %s", tree_spec)
  return(hasErrored, passed, total)

def test():
  right = getRightTree()
  rt = getTreeSpec(right, RIGHT)
  print('Testing Right Tree Evaluation')
  hasErrored1, passed1, total1 = test_tree(rt)
  left = getLeftTree()
  lt = getTreeSpec(left, LEFT)
  print("Testing Left Tree Evaluation")
  hasErrored2, passed2, total2 = test_tree(lt)
  if(hasErrored1 or hasErrored2):
    print('tests completed with errors')
  print("Tests completed {t}.  Tests passed: {p} passing rate: {pr:00.02f}%".format(
    t=total1+total2,
    p=passed1+passed2,
    pr=((passed1 + passed2)/(total1+total2)) * 100
  ))

if __name__ == '__main__':
  test()