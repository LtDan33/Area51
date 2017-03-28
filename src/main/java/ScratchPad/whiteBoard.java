package ScratchPad;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by Dan on 02/24/17.
 */
public class whiteBoard {
    public static void main(String[] args) {
        double mealCost = 12.00; // original meal price
        int tipPercent = 20; // tip percentage
        int taxPercent = 8; // tax percentage

        // Write your calculation code here.
        double tipCost=(mealCost*tipPercent)/100;
        double taxCost=(mealCost*taxPercent)/100;
        mealCost = mealCost+tipCost+taxCost;

        // cast the result of the rounding operation to an int and save it as totalCost
        int totalCost = (int) Math.round(mealCost);

        // Print your result
        System.out.println(totalCost);
    }

}
