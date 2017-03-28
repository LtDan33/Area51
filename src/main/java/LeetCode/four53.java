package LeetCode;

import org.junit.Assert;
import org.junit.Test;

import java.util.Arrays;

/**
 * Created by Dan on 02/13/17.
 * Given a non-empty integer array of size n, find the minimum number of moves required to make all array elements equal, where a move is incrementing n - 1 elements by 1.

 Example:

 Input:
 [1,2,3]

 Output:
 3

 Explanation:
 Only three moves are needed (remember each move increments two elements):

 [1,2,3]  =>  [2,3,3]  =>  [3,4,3]  =>  [4,4,4]
 *
 */
public class four53 {
    public int minMoves(int[] nums) {
        if (nums.length == 1) return 0;

        int steps=0;
        // allEqual= false;

        while(true){
            Arrays.sort(nums);
            if(nums[0]==nums[nums.length-1]) break;
            System.out.println("1");
            for(int i=0; i<=nums.length-2; i++){
                System.out.println("2");
                nums[i]++;
            }
            System.out.println("3");
            steps++;

        }

        return steps;
    }


    @Test
    public void testArray(){
        int[] testArray= {1,2};

        Assert.assertEquals(1,minMoves(testArray));
    }

}
