# 16. 二叉树的层序遍历（Binary Tree Level Order Traversal）· 中等

给定二叉树的根节点 `root`，返回其节点值自底向上或自顶向下的「层序遍历」（逐层从左到右，每层为一个数组）。

## 示例

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

## 考点

- BFS（队列），O(n)。

## 代码实现

[Go 实现](../solutions/p16_binary_tree_level_order_traversal.go)

[单元测试](../solutions/p16_binary_tree_level_order_traversal_test.go)
