package LeetCode;

import org.junit.Test;

import java.util.Arrays;

/**
 * Created by Dan on 03/24/17.
 */
public class testReverseString {
    @Test
    public void testReverse(){
        char[] arr = {'D','a','n'};

        reverseString.flipWord(arr,0,2);

    }

    @Test
    public void testReverseLarger(){
        String sTemp="Dan reverse";

        reverseString.reverseWords(sTemp.toCharArray());
    }

    @Test
    public void testReverseLargerHW(){
        String sTemp="hello world!";

        reverseString.reverseWords(sTemp.toCharArray());
    }


}
