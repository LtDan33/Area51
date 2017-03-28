package LeetCode;

import java.util.Arrays;

/**
 * Created by Dan on 03/24/17.
 */
public class reverseString {

    public static void main(String[] args) {
        String sTemp = "Dan reverse";

        reverseWords(sTemp.toCharArray());
    }

    public static void reverseWords(char[] s) {

        int runner = s.length - 1;
        for (int i = 0; i < s.length / 2; i++) {
            char temp = s[i];
            s[i] = s[runner];
            s[runner--] = temp;
        }

        int start = 0;
        for (int i = 0; i < s.length; i++) {
            if (s[i] == ' ' ) {
                flipWord(s, start, i - 1);
                start = i + 1;
            }
            if(i == (s.length - 1)){
                flipWord(s, start, i);
            }
        }
        System.out.println(Arrays.toString(s));
    }

    public static void flipWord(char[] arr, int start, int end) {
        int halfWayInArray = (start + end) / 2;
        for (int i = start; i <= halfWayInArray; i++) {
            char temp = arr[i];
            arr[i] = arr[end];
            arr[end--] = temp;
        }
    }
}
