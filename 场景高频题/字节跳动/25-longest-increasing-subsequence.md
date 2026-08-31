# 25. 最长递增子序列（Longest Increasing Subsequence）· 中等

给定一个整数数组 `nums`，找到其中最长的严格递增子序列的长度。子序列不要求连续。

## 示例

```
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列为 [2,3,7,101]。
```

## 考点

- 动态规划 O(n²) 或贪心 + 二分 O(n log n)。

## 代码实现

[Go 实现](../../solutions/p25_longest_increasing_subsequence.go)

[单元测试](../../solutions/p25_longest_increasing_subsequence_test.go)
