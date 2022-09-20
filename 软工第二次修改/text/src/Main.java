import IO.IOUtils;
import hanlp.hanlp;
import simhash.simhash;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args)
    {
        IOUtils IOU = new IOUtils();
        hanlp han = new hanlp();
       String s =IOU.readTxt(args[0]);
       String s2 =IOU.readTxt(args[1]);
        ArrayList<String> term = han.separate(s);
        ArrayList<String> term2 = han.separate(s2);
        simhash sim = new simhash(64,term);
        simhash sim2 = new simhash(64,term2);
        System.out.println(sim.hammingDistance(sim2));
        System.out.println(sim.getSemblance(sim2));




    }
}