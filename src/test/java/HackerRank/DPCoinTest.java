package HackerRank;

import HackerRank.CTCISection.DPCoin;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

/**
 * Created by Dan on 03/23/17.
 */
public class DPCoinTest {

    public int[] coins;

    @Before
    public void setUp() {
//        coins = new int[]{1, 2, 3};
        coins = new int[]{41, 34, 46, 9, 37, 32, 42, 21, 7, 13, 1, 24, 3, 43, 2, 23, 8, 45, 19, 30, 29, 18, 35, 11};
    }

    @Test
    public void testDPCoins() {
        System.out.println(DPCoin.findChange(coins, 10));
    }

    @Test
    public void testDPCoins2() {
        Assert.assertEquals(15685693, DPCoin.findChange(coins, 250));

    }
}
