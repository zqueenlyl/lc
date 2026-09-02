# 17. LRU 缓存（LRU Cache）· 中等

设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构，实现以下操作：

- `get(key)`：若 key 存在则返回其值，否则返回 -1。
- `put(key, value)`：插入或更新。当缓存容量达到上限时，删除最近最少使用的键。

要求 `get` 和 `put` 均以 O(1) 平均时间复杂度运行。

## 示例

```
输入：
["LRUCache","put","put","get","put","get","put","get","get","get"]
[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
输出：[null,null,null,1,null,-1,null,-1,3,4]
```

## 考点

- 哈希表 + 双向链表，O(1)。

## 代码实现

[Go 实现](../solutions/p17_lru_cache.go)

[单元测试](../solutions/p17_lru_cache_test.go)
