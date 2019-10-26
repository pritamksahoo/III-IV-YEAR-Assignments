def merge(arr, start, mid, end):
	left, right = start, mid+1
	temp_arr, no_inv = [], 0

	while left <= mid and right <= end:
		if arr[left] <= arr[right]:
			temp_arr.append(arr[left])
			left = left + 1
		else:
			temp_arr.append(arr[right])
			right = right + 1

			no_inv = no_inv + (mid - left + 1)

	while left <= mid:
		temp_arr.append(arr[left])
		left = left + 1

	while right <= end:
		temp_arr.append(arr[right])
		right = right + 1

	arr = temp_arr.copy()
	# print(no_inv, arr)
	return no_inv


def count_inversions(arr, start, end):
	if start < end:
		mid = (start+end)//2

		left_inv = count_inversions(arr, start, mid)
		right_inv = count_inversions(arr, mid+1, end)
		cur_inv = merge(arr, start, mid, end)

		return (left_inv + right_inv + cur_inv)
	else:
		return 0


if __name__ == '__main__':
	no_elements = int(input().strip())

	arr = list(map(int, input().split()))

	no_of_inversions = count_inversions(arr, 0, no_elements-1)

	print("No. of Inversions : ", no_of_inversions)