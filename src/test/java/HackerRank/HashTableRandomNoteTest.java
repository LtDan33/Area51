package HackerRank;

import HackerRank.CTCISection.HashTablesRansomNote;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.Random;

/**
 * Created by Dan on 03/13/17.
 */
public class HashTableRandomNoteTest {

    @Test
    public void testHash(){

        String input = " 2 2 This Will Test Things";
        InputStream in = new ByteArrayInputStream(input.getBytes());
        System.setIn(in);

        HashTablesRansomNote.Solution();
        Assert.assertTrue(true);
    }

}
