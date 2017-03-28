import java.util.*;

/**
 * Created by Dan on 03/11/17.
 */
public class SXSW {

    public static void main(String[] args) {
        List<String> temp = new ArrayList<String>();
        temp.add("23:59");
        temp.add("00:00");

//        temp.add("12:12");
//        temp.add("00:13");
//        temp.add("05:31");
//        temp.add("22:08");
//        temp.add("00:35");

        System.out.println(findMinDifference2(temp));
//        System.out.println(reverseStr("abcdefg", 2));
//        System.out.println(reverseStr("abcd", 4));
//        System.out.println(reverseStr("abcdefg", 8));
    }


    public static int findMinDifference2(List<String> timePoints) {
        Collections.sort(timePoints);
        int min = 24*60+diff(timePoints.get(0), timePoints.get(timePoints.size()-1));

        for (int i=1; i<timePoints.size(); i++) {
            min = Math.min(min, diff(timePoints.get(i), timePoints.get(i-1)));
        }
        return min;
    }
    private static int diff(String a, String b) {
        int hh = Integer.parseInt(a.substring(0,2))-Integer.parseInt(b.substring(0,2));
        int mm = Integer.parseInt(a.substring(3))-Integer.parseInt(b.substring(3));

        return 60*hh+mm;
    }

    public static int  findMinDifference(List<String> timePoints) {

        int difference = Integer.MAX_VALUE;

        List<Integer> minList = new ArrayList<Integer>();

        for(String s:timePoints){
            String[] temp= s.split(":");
            String hours= temp[0];
            String minutes= temp[1];

            Integer tempInt = (Integer.parseInt(hours)*60)+Integer.parseInt(minutes);

            minList.add(tempInt);
            if(tempInt>(800)){
                minList.add((24*60)-tempInt);
            }
        }

        Collections.sort(minList);


        // Find the min diff by comparing adjacent
        // pairs in sorted array
        for (int i=0; i<minList.size()-1; i++)
            if (minList.get(i+1) - minList.get(i) < difference) {
                difference = minList.get(i + 1) - minList.get(i);
            }

        // Return min diff
        return difference;
    }







    //        System.out.println(reverseStr("abcdefg", 2));
//        System.out.println(reverseStr("abcd", 4));
//        System.out.println(reverseStr("abcdefg", 8));
    public static String reverseStr(String s, int k) {
        if ((k <= 0)) {
            return s;
        }

        StringBuilder wholeWord = new StringBuilder();
        StringBuilder sb = new StringBuilder();
        char[] charArray = s.toCharArray();
        boolean reverseStuff = true;
        boolean done = false;

        for (int i = 0; i < charArray.length; i++) {
            if ((i % k == 0) && (i != 0) || (i == charArray.length - 1)) {
                if((i == charArray.length - 1) && (sb.length()!=k)){
                    sb.append(charArray[i]);
                    done=true;
                }
                if (reverseStuff) {
                    wholeWord.append(sb.reverse());
                } else {
                    wholeWord.append(sb);
                }
                if ((i == charArray.length - 1) && (!done)){
                    wholeWord.append(charArray[i]);
                }
                reverseStuff = !reverseStuff;
                sb.setLength(0);
            }
            sb.append(charArray[i]);
        }
        return wholeWord.toString();
    }

    public static void solution() {
        HashMap<String, String> map = new HashMap<String, String>();
        LinkedList<String> ll = new LinkedList<String>();
        ArrayList<String> aL = new ArrayList<String>();


    }
}
