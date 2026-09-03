# 18. 合并 K 个升序链表（Merge k Sorted Lists）· 困难

给定一个链表数组，每个链表都已按升序排列，请将所有链表合并为一个升序链表并返回。

## 示例

```
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
```

## 考点

- 优先队列（最小堆）O(n log k) 或分治两两合并。

## 代码实现

[Go 实现](../solutions/p18_merge_k_sorted_lists.go)

[单元测试](../solutions/p18_merge_k_sorted_lists_test.go)
