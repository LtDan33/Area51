package LeetCode;


import java.util.HashMap;

/**
 * Created by Dan on 03/21/17.
 */
public class Amazon {

    public int firstUniqChar(String s) {
        HashMap<Character,Integer > map = new HashMap<>();
        char[] arr = s.toCharArray();

        for(int i=0; i<arr.length;i++){
            char c = arr[i];
            if(map.containsKey(c)){
                map.put(c, map.get(c)+1);
            }
            else{
                map.put(c,1);
            }
        }
        for(int i=0; i<arr.length;i++){
            char c = arr[i];
            if(map.get(c)==1){
                return i;
            }
        }
        return -1;
    }
}
