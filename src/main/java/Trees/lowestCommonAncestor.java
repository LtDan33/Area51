package Trees;

/**
 * Created by Dan on 03/28/17.
 */
public class lowestCommonAncestor {

    public static Node findCommonAncestor(Node root, int value1, int value2){

        if(root==null){
            return null;
        }

        if(root.data==value1 || root.data == value2){
            return root;
        }

        Node leftNode = findCommonAncestor(root.left, value1, value2);
        Node rightNode = findCommonAncestor(root.right, value1, value2);

        if(leftNode==null || rightNode== null){
            return (leftNode==null)?rightNode:leftNode;
        }

        return root;
    }
}
