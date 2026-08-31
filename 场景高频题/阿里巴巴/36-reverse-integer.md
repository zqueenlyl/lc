# 36. 整数反转（Reverse Integer）· 中等

给定一个 32 位有符号整数 `x`，返回将其数字部分反转后的结果。若反转后超出 32 位有符号整数范围 `[-2^31, 2^31-1]`，则返回 0。

## 示例

```
输入：x = 123
输出：321

输入：x = -120
输出：-21
```

## 考点

- 逐位取模反转 + 溢出判断，O(log n)。

## 代码实现

[Go 实现](../../solutions/p36_reverse_integer.go)

[单元测试](../../solutions/p36_reverse_integer_test.go)
