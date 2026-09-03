# 32. 合并区间（Merge Intervals）· 中等

给定一个区间数组 `intervals`，其中每个区间为 `[start, end]`，请合并所有重叠的区间，返回一个不重叠的区间数组。

## 示例

```
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
```

## 考点

- 按起点排序 + 遍历合并，O(n log n)。

## 代码实现

[Go 实现](../../solutions/p32_merge_intervals.go)

[单元测试](../../solutions/p32_merge_intervals_test.go)
