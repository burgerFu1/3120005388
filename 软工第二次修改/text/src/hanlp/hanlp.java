package hanlp;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class hanlp {
    public ArrayList<String>   separate(String txt){
        File file = new File("D:\\idea_project\\text\\src\\hanlp\\cn_stopwords.txt");//使用IO输入停用词文件
        ArrayList<String> stopword = new ArrayList();
        try {
            BufferedReader br = new BufferedReader(new FileReader(file));
            String string1 = null;
            while ((string1 = br.readLine()) != null) {//使用readLine方法，一次读一行 读取停用词
                stopword.add(string1); //把文件转换为字符串形式
            }
            br.close();
        }catch (IOException e) {
            throw new RuntimeException(e);
        }

    HanLP.Config.ShowTermNature = false;        //隐藏词性
    List<Term> termList = HanLP.segment(txt);   //利用HanLP分词器进行分词
    ArrayList<String> TermList = new ArrayList();
    for (int i=0;i<termList.size();i++){
        TermList.add(termList.get(i).toString());
    }
        TermList.removeAll(stopword);   //过滤停用词
       return TermList;
    }


}
