package LeetCode;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

/**
 * Created by Dan on 03/24/17.
 */
public class RightTree {


    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> rightView = new ArrayList<>();
        if(root==null){
            return rightView;
        }

//        LinkedList<TreeNode> LLTree = new LinkedList<>();

//        LLTree.add(root);

//        while(!LLTree.isEmpty()){
//            TreeNode tempNode= LLTree.remove();
//            if(root.right!=null){
//                LLTree.add(root.right);
//            }
//            if(root.left!=null){
//                LLTree.add(root.left);
//            }
//        }
        rightSideView(root,rightView,0 );

        return rightView;
    }

    private static void rightSideView(TreeNode root , List<Integer> rightView, int level){
        if(root ==null){
            return;
        }

        if(rightView.size()== level){
            rightView.add(root.val);
        }

        rightSideView(root.right, rightView, level+1);
        rightSideView(root.left, rightView, level+1);
    }
}
