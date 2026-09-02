# 22. 搜索旋转排序数组（Search in Rotated Sorted Array）· 中等

给定一个「原本升序、在某个未知下标处旋转后」的数组 `nums`（元素互不相同）和目标值 `target`，返回 `target` 在数组中的下标，若不存在则返回 -1。要求时间复杂度 O(log n)。

## 示例

```
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4

输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
```

## 考点

- 二分查找，判断有序半边，O(log n)。

## 解题思路

以 `nums[0]` 为基准，先判定目标值所在半区，再进行一次二分查找（无需先找旋转点）。

1. **判定目标半区 A**：比较 `target` 与 `nums[0]`——`target >= nums[0]` 则 A 为左半区（较大值段），否则 A 为右半区（较小值段）。
2. **二分查找**：取中间值 `current`，`current >= nums[0]` 表示 `current` 在左半区，否则在右半区：
   - 先判定 `current == target`，是则直接返回；
   - 若 `current` 与 `target` 同半区（该半区有序），按 `current` 与 `target` 的大小决定向左或向右二分；
   - 若 `current` 与 `target` 异半区，直接向 A（目标所在）半区方向收缩。

复杂度：单次二分，O(log n)。

## 代码实现

[Go 实现](../../solutions/p22_search_in_rotated_sorted_array.go)

[单元测试](../../solutions/p22_search_in_rotated_sorted_array_test.go)
