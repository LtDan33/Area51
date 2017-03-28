package HackerRank.CTCISection;

import java.util.HashMap;
import java.util.HashSet;

/**
 * Created by Dan on 03/23/17.
 */
public class DPCoin {
    static public long findChange(int[] coins, int money) {

        HashMap<Integer,Integer> map = new HashMap<>();

        HashSet<Integer> set = new HashSet<>();

        for(Integer i:set){
            int returnVal= i;
        }

        long[] values = new long[money+1];
        values[0]= 1;

        for(int coin: coins){
            for(int i=coin; i<values.length; i++){
                values[i]+=values[i-coin];
            }
        }
        return values[money];
    }
}
