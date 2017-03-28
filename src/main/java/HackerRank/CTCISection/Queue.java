package HackerRank.CTCISection;

/**
 * Created by Dan on 03/13/17.
 */
import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Queue {
    public static void main(String[] args) {
        MyQueue<Integer> queue = new MyQueue<Integer>();

        Scanner scan = new Scanner(System.in);
        int n = scan.nextInt();

        for (int i = 0; i < n; i++) {
            int operation = scan.nextInt();
            if (operation == 1) { // enqueue
                queue.enqueue(scan.nextInt());
            } else if (operation == 2) { // dequeue
                queue.dequeue();
            } else if (operation == 3) { // print/peek
//                System.out.println(queue.peek());
            }
        }
        scan.close();
    }

    private static class MyQueue<T> {
        Stack thisStack;
        Object beginning;
        Object end;


        public MyQueue(){
            thisStack = new Stack();
        }

        public void enqueue(int value){
            thisStack.push(value);
        }
        public void dequeue(){

        }
    }
}
