package solution

// 22. 搜索旋转排序数组（Search in Rotated Sorted Array）· 中等
// 在旋转后的有序数组中二分查找 target，返回下标，不存在返回 -1。
//
// 思路（一次二分）：以 nums[0] 为基准判断中间值所在半区，
// 结合 target 所在半区决定收缩方向，O(log n)。

func Search(nums []int, target int) int {
	n := len(nums)
	if n == 0 {
		return -1
	}

	first := nums[0]
	// 目标值所在半区：target >= first 在左半区（较大值段），否则在右半区（较小值段）。
	targetInLeft := target >= first

	lo, hi := 0, n-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		current := nums[mid]

		// 1. 先判定是否等于目标值，是则直接退出。
		if current == target {
			return mid
		}

		// current 所在半区：>= first 在左半区，否则在右半区。
		currentInLeft := current >= first

		if currentInLeft == targetInLeft {
			// 2. current 与 target 同半区（该半区有序），按大小标准二分。
			if current < target {
				lo = mid + 1
			} else {
				hi = mid - 1
			}
		} else {
			// 3. current 与 target 异半区，直接向 A（target 所在）半区方向收缩。
			if targetInLeft {
				hi = mid - 1 // target 在左半区，mid 在右半区，向左
			} else {
				lo = mid + 1 // target 在右半区，mid 在左半区，向右
			}
		}
	}
	return -1
}
