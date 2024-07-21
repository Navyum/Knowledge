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

func main() {
	array := []int{7, 4, 3, 3, 6, 9, 1, 5}
	fmt.Println("origin:", array)
	//BubbleSort(array)
	//SelectSort(array)
	InsertSort(array)
}
