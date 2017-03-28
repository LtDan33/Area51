/**
 * Created by Dan on 01/25/17.
 */
public class quickSort {

    public void sort(int[] nums, int left, int right){

        if(nums == null || nums.length ==0){
            return;
        }

        int index= quicksorting(nums, left, right);

        //sort the right half
        if(left < index - 1){
            quicksorting(nums, index, right);
        }
        //sort the right half
        if(index < right){
            quicksorting(nums, index, right);
        }
    }

    public static int quicksorting(int[] arr, int left, int right){
        int pivot = arr[(left+right)/2];
//        [sxxxxxpxxxxxe]
        while (left<right) {
            //what if you never get left > ? Actually would get to pivot eventually
            while(arr[left]<pivot){
                left++;
            }

            while(arr[right]>pivot){
                right--;
            }

            if(left<= right) {
                swap(arr, left, right);
                left++;
                right--;
            }
        }
        return left;
    }

    public static void swap(int[] arr, int start, int end){
        int temp = arr[start];
        arr[start]= arr[end];
        arr[end]= temp;
    }
}
