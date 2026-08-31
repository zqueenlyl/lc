# 09. 对称二叉树（Symmetric Tree）· 简单

给定二叉树的根节点 `root`，检查它是否是轴对称的（镜像对称）。

## 示例

```
输入：root = [1,2,2,3,4,4,3]
输出：true

输入：root = [1,2,2,null,3,null,3]
输出：false
```

## 考点

- 递归或迭代，比较左右子树镜像，O(n)。

## 代码实现

[Go 实现](../solutions/p09_symmetric_tree.go)

[单元测试](../solutions/p09_symmetric_tree_test.go)
