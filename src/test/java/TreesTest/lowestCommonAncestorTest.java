package TreesTest;

import Trees.Node;
import Trees.lowestCommonAncestor;
import org.junit.Before;
import org.junit.Test;

/**
 * Created by Dan on 03/28/17.
 */
public class lowestCommonAncestorTest {

    Node root;

    @Before
    public void setUp(){
        root = new Node(3);
        root.setLeft(new Node(6));
        root.setRight(new Node(8));

        root.left.setLeft(new Node(2));
        root.left.setRight(new Node(11));

        root.left.right.setLeft(new Node(9));
        root.left.right.setRight(new Node(5));

        root.right.setRight(new Node(13));
    }

    @Test
    public void getCorrectChild(){
        Node answer = lowestCommonAncestor.findCommonAncestor(root, 2, 5);
        System.out.println(answer.data);
    }

}
