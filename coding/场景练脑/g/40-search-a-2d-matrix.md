# 40. 搜索二维矩阵（Search a 2D Matrix）· 中等

给定一个 `m x n` 的矩阵，每行从左到右升序排列，且每行第一个整数大于上一行最后一个整数。给定目标值 `target`，判断是否在矩阵中，要求 O(log(mn))。

## 示例

```
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true
```

## 考点

- 将矩阵视为一维有序数组二分，或从右上角搜索，O(log(mn))。

## 代码实现

[Go 实现](../../solutions/p40_search_a_2d_matrix.go)

[单元测试](../../solutions/p40_search_a_2d_matrix_test.go)
