# 11. 无重复字符的最长子串（Longest Substring Without Repeating Characters）· 中等

给定一个字符串 `s`，找出其中不含重复字符的最长子串的长度。

## 示例

```
输入：s = "abcabcbb"
输出：3
解释：最长子串为 "abc"。

输入：s = "bbbbb"
输出：1
```

## 考点

- 滑动窗口 + 哈希表，O(n)。
