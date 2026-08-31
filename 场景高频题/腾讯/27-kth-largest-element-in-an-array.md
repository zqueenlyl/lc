# 27. 数组中的第 K 个最大元素（Kth Largest Element in an Array）· 中等

给定整数数组 `nums` 和整数 `k`，返回数组中第 `k` 个最大的元素（注意是排序后第 k 大，而非第 k 个不同元素）。

## 示例

```
输入：nums = [3,2,1,5,6,4], k = 2
输出：5
```

## 考点

- 快速选择（平均 O(n)）或大小为 k 的小顶堆（O(n log k)）。

## 代码实现

[Go 实现](../../solutions/p27_kth_largest_element_in_an_array.go)

[单元测试](../../solutions/p27_kth_largest_element_in_an_array_test.go)
