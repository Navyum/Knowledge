package main

func removeDuplicates(nums []int) int {
	i, j := 0, len(nums)-1

	for i < j {
		for k := 0; k < i; k++ {
			if nums[k] == nums[j] {
				j--
				break
			} else {
				if k == i-1 {
					i++
				}
			}
		}
	}
	return i
}

func main() {
	nums := []int{1, 1, 2}
	removeDuplicates(nums)
}
