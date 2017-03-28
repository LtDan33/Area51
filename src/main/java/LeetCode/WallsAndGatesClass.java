package LeetCode;

import java.util.LinkedList;
import java.util.Queue;

/**
 * Created by Dan on 03/21/17.
 */
public class WallsAndGatesClass {

    LinkedList<valueSet> LL;

    public void wallsAndGates(int[][] rooms) {
        LL= new LinkedList<>();
        for (int i = 0; i < rooms[0].length; i++) {
            for (int k = 0; k < rooms.length; k++) {
                if(rooms[i][k]==0) {
                        LL.add(new valueSet(i,k));
                }
            }
        }
        BFSFindDoor(LL, rooms);

        System.out.println("Done");
    }

    private void BFSFindDoor(LinkedList<valueSet> LL, int[][] rooms) {
        while (!LL.isEmpty()) {
            valueSet valPair = LL.removeFirst();

            if (valPair.x < 0 || valPair.x > rooms[0].length-1 || valPair.y < 0 || valPair.y > rooms.length-1) {
                continue;
            }

            int value = rooms[valPair.y][valPair.x];

            switch (value) {
                case -1:
                    continue;
                case 0:
                    continue;
                case Integer.MAX_VALUE:

                    if (valPair.x > 0)
                        LL.add(new valueSet(valPair.x - 1, valPair.y));
                    if (valPair.y > 0)
                        LL.add(new valueSet(valPair.x, valPair.y - 1));
                    if (valPair.y < rooms.length - 1)
                        LL.add(new valueSet(valPair.x, valPair.y + 1));
                    if (valPair.x < rooms.length - 1)
                        LL.add(new valueSet(valPair.x + 1, valPair.y));
                    continue;
                default : continue;
            }
        }
    }

    private int spacesAway(valueSet valPair, int xVal, int yVal) {
        int x = Math.abs(valPair.x - xVal);
        int y = Math.abs(valPair.y - yVal);
        return x + y;
    }

    class valueSet {
        int x;
        int y;

        valueSet(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }
}


//    private static final int EMPTY = Integer.MAX_VALUE;
//    private static final int GATE = 0;
//    private static final List<int[]> DIRECTIONS = Arrays.asList(
//            new int[] { 1,  0},
//            new int[] {-1,  0},
//            new int[] { 0,  1},
//            new int[] { 0, -1}
//    );
//
//    public void wallsAndGates(int[][] rooms) {
//        int m = rooms.length;
//        if (m == 0) return;
//        int n = rooms[0].length;
//        Queue<int[]> q = new LinkedList<>();
//        for (int row = 0; row < m; row++) {
//            for (int col = 0; col < n; col++) {
//                if (rooms[row][col] == GATE) {
//                    q.add(new int[] { row, col });
//                }
//            }
//        }
//        while (!q.isEmpty()) {
//            int[] point = q.poll();
//            int row = point[0];
//            int col = point[1];
//            for (int[] direction : DIRECTIONS) {
//                int r = row + direction[0];
//                int c = col + direction[1];
//                if (r < 0 || c < 0 || r >= m || c >= n || rooms[r][c] != EMPTY) {
//                    continue;
//                }
//                rooms[r][c] = rooms[row][col] + 1;
//                q.add(new int[] { r, c });
//            }
//        }
//    }
