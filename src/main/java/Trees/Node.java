package Trees;

/**
 * Created by Dan on 03/28/17.
 */
public class Node {
    public int data;
    public Node left;
    public Node right;

    public Node(int data){
        this.data = data;
    }

    public void setLeft(Node left){
     this.left = left;
    }

    public void setRight(Node right){
        this.right = right;
    }
}
