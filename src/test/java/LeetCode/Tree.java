package LeetCode;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static LeetCode.RightTree.rightSideView;

/**
 * Created by Dan on 03/24/17.
 */
public class Tree {

    TreeNode root;

    @Before
    public void testReverse(){
        root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);

    }

    @Test
    public void testTree(){
        List<Integer> rightView= rightSideView(root);
        System.out.println(rightView.toString());
    }

}
