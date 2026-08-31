# 07. 最长公共前缀（Longest Common Prefix）· 简单

编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 `""`。

## 示例

```
输入：strs = ["flower","flow","flight"]
输出："fl"

输入：strs = ["dog","racecar","car"]
输出：""
```

## 考点

- 纵向扫描或横向扫描，O(S)，S 为所有字符总数。
