package HackerRank.CTCISection;


/**
 * Created by Dan on 03/13/17.
 */
public class StringsMakingAnagrams {
    public static int numberNeeded(String first, String second) {
        if(first.length()==0 || second.length()==0){
            return first.length()==0? second.length(): first.length();
        }

        int totalValue=0;

        StringBuilder sbFirst = new StringBuilder(first);
        StringBuilder sbSecond = new StringBuilder(second);
        boolean found=false;

        for(int i=0; i<sbFirst.length();i++){
            for(int k=0; k<sbSecond.length();k++){
                if(sbFirst.charAt(i)==sbSecond.charAt(k)){
                    sbSecond.deleteCharAt(k);
                    found=true;
                    break;
                }
            }
            if(!found){
                totalValue++;

            }
            else{
                found =false;
            }
        }
        totalValue+=sbSecond.length();

        return totalValue;
    }

    public static void main(String[] args) {

//        System.out.println(StringsMakingAnagrams.numberNeeded("ab","acbfg"));
//        System.out.println(StringsMakingAnagrams.numberNeeded("acbfg","ab"));
        System.out.println(StringsMakingAnagrams.numberNeeded("aabbccdd","abcd"));
        //Should be 102
//        System.out.println(StringsMakingAnagrams.numberNeeded("imkhnpqnhlvaxlmrsskbyyrhwfvgteubrelgubvdmrdmesfxkpykprunzpustowmvhupkqsyjxmnptkcilmzcinbzjwvxshubeln"
//                ,"wfnfdassvfugqjfuruwrdumdmvxpbjcxorettxmpcivurcolxmeagsdundjronoehtyaskpwumqmpgzmtdmbvsykxhblxspgnpgfzydukvizbhlwmaajuytrhxeepvmcltjmroibjsdkbqjnqjwmhsfopjvehhiuctgthrxqjaclqnyjwxxfpdueorkvaspdnywupvmy"));


//        Scanner in = new Scanner(System.in);
//        String a = in.next();
//        String b = in.next();
//        System.out.println(numberNeeded(a, b));
    }

}
