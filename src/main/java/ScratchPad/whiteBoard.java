package ScratchPad;

import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by Dan on 02/24/17.
 */
public class whiteBoard {
    public static void main(String[] args) {
        double mealCost = 12.00; // original meal price
        int tipPercent = 20; // tip percentage
        int taxPercent = 8; // tax percentage

        // Write your calculation code here.
        double tipCost=(mealCost*tipPercent)/100;
        double taxCost=(mealCost*taxPercent)/100;
        mealCost = mealCost+tipCost+taxCost;

        // cast the result of the rounding operation to an int and save it as totalCost
        int totalCost = (int) Math.round(mealCost);

        // Print your result
        System.out.println(totalCost);
    }

    public boolean isPalindromeSol(ListNode head) {
        ListNode fast = head, slow = head;
        while (fast != null && fast.next != null) {
            fast = fast.next.next;
            slow = slow.next;
        }
        if (fast != null) { // odd nodes: let right half smaller
            slow = slow.next;
        }
        slow = reverseLL(slow);
        fast = head;

        while (slow != null) {
            if (fast.val != slow.val) {
                return false;
            }
            fast = fast.next;
            slow = slow.next;
        }
        return true;
    }

    public boolean isPalindromeSol2(ListNode head) {
        if(head == null)
            return true;

        ListNode p = head;
        ListNode prev = new ListNode(head.val);

        while(p.next != null){
            ListNode temp = new ListNode(p.next.val);
            temp.next = prev;
            prev = temp;
            p = p.next;
        }

        ListNode p1 = head;
        ListNode p2 = prev;

        while(p1!=null){
            if(p1.val != p2.val)
                return false;

            p1 = p1.next;
            p2 = p2.next;
        }

        return true;
    }


    //    *****************CTCI solution
    public boolean isPalindromeCTCI(ListNode head){
        ListNode reversed = reverseAndCloneCTCI(head);

        while(head!=null){
            if(head.val != reversed.val)
                return false;

            head = head.next;
            reversed = reversed.next;
        }
        return true;
    }

    public static ListNode reverseAndCloneCTCI(ListNode node){
        ListNode head = null;

        while (node!= null){
            ListNode temp = new ListNode(node.val);
            temp.next = head;
            head = temp;
            node = node.next;
        }
        return head;
    }

    public boolean isPalindrome(ListNode head) {
        boolean isPalindrome= false;

        ListNode reverseHead = reverseLL(head);

        ListNode temp;
        ListNode temp2;

        do{
            if(head.val != reverseHead.val){
                return false;
            }
            head = head.next;
            reverseHead = reverseHead.next;

        }
        while(head!= null);
        return true;
    }

    ListNode reverseLL(ListNode reverseHead){
        ListNode current=reverseHead;
        ListNode prev=null;
        ListNode next=null;

        while(current!= null){
            next = current.next;
            current.next = prev;
            prev= current;
            current= next;
        }
        return prev;
    }

    @Test
    public void test1(){

        ListNode head = new ListNode(1);
        ListNode second = new ListNode(1);
        ListNode third = new ListNode(2);
        ListNode fourth = new ListNode(1);

        head.next = second;
        second.next = third;
        third.next = fourth;

//        Assert.assertTrue(isPalindrome(head));
        Assert.assertFalse(isPalindromeCTCI(head));
    }

}
