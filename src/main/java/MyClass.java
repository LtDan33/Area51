import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.stream.IntStream;

/**
 * Created by Dan on 10/05/16.
 */
public class MyClass {

    int test =0;

    public static void main(String[] args)
    {
        String A ="caaa";
        String B ="bb";

        CapFirstLetter(A,B);
//        a negative integer, zero, or a positive integer as the
//            *          specified String is greater than, equal to, or less
//            *          than this String, ignoring case considerations.

    }

    private static void CapFirstLetter(String A, String B){
        StringBuilder tempA = new StringBuilder(A);
        StringBuilder tempB = new StringBuilder(B);
        tempA.setCharAt(0, Character.toUpperCase(tempA.charAt(0)));
        tempB.setCharAt(0, Character.toUpperCase(tempB.charAt(0)));

        System.out.println(tempA.toString());
        System.out.println(tempB.toString());
    }


    private static class Stack
    {
        private LinkedList<Character> stack;

        public Stack()
        {
            this.stack = new LinkedList<Character>();
        }
        public void push(char c)
        {
            stack.addFirst(c);
        }
        public void pop()
        {
            stack.removeFirst();
        }
        public char peek() {
            return stack.getFirst();
        }
        public int size() {
            return stack.size();
        }
        public String toString()
        {
            return stack.toString();
        }
    }

}
