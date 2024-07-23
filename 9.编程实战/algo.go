package main

import "fmt"

func BubbleSort(array []int) {
	len := len(array)

	//找第i个位置的值,[0,i]为未排序区间
	for i := len - 1; i > 0; i-- {

		//遍历列表，两两对比
		for j := 0; j < i; j++ {

			if array[j] > array[j+1] {
				array[j], array[j+1] = array[j+1], array[j] //swap
			}
			//fmt.Println(array)
		}
		//fmt.Println("----")
	}
	fmt.Println(array)
}

func SelectSort(array []int) {
	len := len(array)

	//找第i个位置的值, [i,len)为未排序区间。最后一个元素在前一个元素插入时自动有序
	for i := 0; i < len-1; i++ {

		min := i

		//遍历列表，找出未排序区间(i,len]的最小值索引min
		for j := i + 1; j < len; j++ {
			if array[j] < array[min] {
				min = j
			}
		}
		array[i], array[min] = array[min], array[i]
	}
	fmt.Println(array)

}

func InsertSort(array []int) {
	len := len(array)

	//找第i个位置的值, (i,len]为未排序区间。第一个元素默认已经排序
	for i := 1; i < len; i++ {
		fmt.Println(array[i])
		// 在已排序的[0,i]中找到插入位置，从后往前找更方便移动位置
		for j := i - 1; j >= 0; j-- {
			if array[j] > array[j+1] {
				array[j+1], array[j] = array[j], array[j+1]
			} else {
				break
			}

			fmt.Println(array)
		}
	}
	fmt.Println(array)
}

//二分查找target元素，有则返回target索引，没有则返回 -1
func BinarySearch(array []int, target int) int {
	i, j := 0, len(array)-1

	for i <= j {
		mid := (j + i) / 2

		if target < array[mid] {
			j = mid - 1
		} else if target > array[mid] {
			i = mid + 1
		} else {
			return mid
		}
	}

	return -1

}

//不存在重复元素，寻找target插入点
func BinarySearchInsert(array []int, target int) int {
	i, j := 0, len(array)-1

	var mid int
	for i <= j {
		// 计算中位数
		mid = (j + i) / 2

		if target < array[mid] {
			j = mid - 1
		} else if target > array[mid] {
			i = mid + 1

			// 元素相等，则该位置为插入点
		} else {
			return mid
		}
	}

	//返回i的位置
	fmt.Println(i, j)
	return i

}

// 存在重复元素时，寻找target插入点
func BinarySearchInsertMulti(array []int, target int) int {
	i, j := 0, len(array)-1

	var mid int
	for i <= j {
		mid = (j + i) / 2
		fmt.Println(i, j, mid)
		if target < array[mid] {
			j = mid - 1
		} else if target > array[mid] {
			i = mid + 1
		} else {
			j = mid - 1
		}
	}

	return i

}

func main() {
	//array := []int{7, 4, 3, 3, 6, 9, 1, 5}
	//fmt.Println("origin:", array)
	//BubbleSort(array)
	//SelectSort(array)
	//InsertSort(array)

	array := []int{1, 3, 4, 5, 8, 10, 28}
	fmt.Println("origin:", array)
	i := BinarySearchInsert(array, 2)
	fmt.Println(i)
}
