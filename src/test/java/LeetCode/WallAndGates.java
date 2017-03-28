package LeetCode;

import org.junit.Before;
import org.junit.Test;

/**
 * Created by Dan on 03/21/17.
 */
public class WallAndGates {

    WallsAndGatesClass wallsAndGates;

    @Before
    public void setUp(){
        wallsAndGates = new WallsAndGatesClass();
    }

    @Test
    public void TestWholeMethod() {
        int[][] inputArr = {{2147483647, -1, 0, 2147483647}, {2147483647, 2147483647, 2147483647, -1}, {2147483647, -1, 2147483647, -1}, {0, -1, 2147483647, 2147483647}};
        wallsAndGates.wallsAndGates(inputArr);
    }
}
