# 23. 复制带随机指针的链表（Copy List with Random Pointer）· 中等

给定一个链表，每个节点包含一个额外随机指针 `random`，指向链表中的任意节点或 `null`。请深拷贝这个链表，返回新链表的头节点。

## 示例

```
输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

## 考点

- 哈希表映射旧节点→新节点，或原地复制（穿插节点）O(n)。

## 代码实现

[Go 实现](../../solutions/p23_copy_list_with_random_pointer.go)

[单元测试](../../solutions/p23_copy_list_with_random_pointer_test.go)
