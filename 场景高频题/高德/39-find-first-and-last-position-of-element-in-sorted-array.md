# 39. 在排序数组中查找元素的第一个和最后一个位置（Find First and Last Position）· 中等

给定一个非递减排序的整数数组 `nums` 和目标值 `target`，返回 `target` 在数组中第一次和最后一次出现的下标；若不存在则返回 `[-1, -1]`。要求 O(log n)。

## 示例

```
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
```

## 考点

- 两次二分查找（找左边界和右边界），O(log n)。

## 代码实现

[Go 实现](../../solutions/p39_find_first_and_last_position_of_element_in_sorted_array.go)

[单元测试](../../solutions/p39_find_first_and_last_position_of_element_in_sorted_array_test.go)
