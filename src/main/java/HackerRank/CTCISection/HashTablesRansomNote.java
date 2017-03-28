package HackerRank.CTCISection;

import java.util.HashMap;
import java.util.Scanner;

/**
 * Created by Dan on 03/13/17.
 */
public class HashTablesRansomNote {

    public static void Solution() {
        Scanner in = new Scanner(System.in);
        int m = in.nextInt();
        int n = in.nextInt();

        HashMap<String, Integer> words = new HashMap<String, Integer>();

        for (int magazine_i = 0; magazine_i < m; magazine_i++) {
            String temp = in.next();
            if (words.containsKey(temp)) {
                words.put(temp, words.get(temp) + 1);
            } else {
                words.put(temp, 1);
            }
        }
        for (int ransom_i = 0; ransom_i < n; ransom_i++) {
            String temp = in.next();
            if (!words.containsKey(temp) || words.get(temp) == 0) {
                System.out.println("No");
                return;
            } else {
                words.put(temp, words.get(temp) - 1);
            }
        }
        System.out.println("Yes");
    }
}
