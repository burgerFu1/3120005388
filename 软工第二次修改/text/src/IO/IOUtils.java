package IO;

import java.io.*;

public class IOUtils {

    public String readTxt(String FIN){
        File file = new File(FIN);
        StringBuffer sb = new StringBuffer();
        try {
            FileInputStream fis = new FileInputStream(file);
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            String line = null;
            while ((line = br.readLine())!= null) {
                sb.append(line);
            }
            br.close();
            fis.close();
        } catch (IOException e){
            e.printStackTrace();
        }
        return  sb.toString();

    }


}
