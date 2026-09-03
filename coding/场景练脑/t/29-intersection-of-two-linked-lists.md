# 29. 相交链表（Intersection of Two Linked Lists）· 简单

给定两个单链表的头节点 `headA` 和 `headB`，找出并返回它们相交的起始节点；若两个链表不相交则返回 `null`。

## 示例

```
输入：listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]
输出：相交节点值为 8
```

## 考点

- 双指针走对方链表，O(m+n)；或用哈希表。

## 代码实现

[Go 实现](../../solutions/p29_intersection_of_two_linked_lists.go)

[单元测试](../../solutions/p29_intersection_of_two_linked_lists_test.go)
