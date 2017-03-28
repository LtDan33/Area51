package HackerRank.CTCISection;

import java.util.Stack;

/**
 * Created by Dan on 03/13/17.
 */
public class Balanced {
    public static boolean Solution(String expression) {
        Stack<Character> stack = new Stack<Character>();

        char[] charArr = expression.toCharArray();

        for (char c : charArr) {
            if (c == '[' || c == '(' || c == '{') {
                stack.push(c);
            } else {
                if(stack.isEmpty()){
                    return false;
                }
                switch (c) {
                    case ']':
                        if (stack.peek() != '[') {
                            return false;
                        }
                        break;
                    case '}':
                        if (stack.peek() != '{') {
                            return false;
                        }
                        break;
                    case ')':
                        if (stack.peek() != '(') {
                            return false;
                        }
                        break;
                }
                stack.pop();
            }
        }
        if (stack.size()>0){
            return false;
        }
        return true;
    }
}
