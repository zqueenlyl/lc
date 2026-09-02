# 03. 合并两个有序链表（Merge Two Sorted Lists）· 简单

将两个升序链表合并为一个新的升序链表并返回。新链表由两个链表的节点拼接而成。

## 示例

```
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

## 考点

- 双指针 + 虚拟头节点，O(m+n)。

## 代码实现

[Go 实现](../solutions/p03_merge_two_sorted_lists.go)

[单元测试](../solutions/p03_merge_two_sorted_lists_test.go)
