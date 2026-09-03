# 24. 二叉树的最近公共祖先（Lowest Common Ancestor of a Binary Tree）· 中等

给定一个二叉树，找到该树中两个指定节点 `p` 和 `q` 的最近公共祖先（LCA）。最近公共祖先定义为：对于有根树 T 的两个节点 p、q，最近公共祖先表示一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大。

## 示例

```
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
```

## 考点

- 递归后序遍历，O(n)。

## 代码实现

[Go 实现](../../solutions/p24_lowest_common_ancestor_of_a_binary_tree.go)

[单元测试](../../solutions/p24_lowest_common_ancestor_of_a_binary_tree_test.go)
