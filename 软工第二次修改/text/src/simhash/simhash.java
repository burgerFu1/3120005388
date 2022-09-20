package simhash;

import com.hankcs.hanlp.tokenizer.lexical.NERecognizer;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class simhash{
    private  int hashbits = 64;//定义hash值的位数
    private BigInteger strSimHash;

   public simhash(ArrayList<String> TermList){

       this.strSimHash = this.simHash(TermList);
   }

   public simhash(int hashbits,ArrayList<String> TermList){
       this.hashbits = hashbits;
       this.strSimHash = this.simHash(TermList);
   }


    public BigInteger  simHash(ArrayList<String> TermList){
       int[] v = new int[this.hashbits];

       //设置超频词限制
        int overcount =  5;
        Map<String,Integer> wordcount = new HashMap<String,Integer>();
        for (String s :TermList){   //对每个分词进行频率统计，根据频率确定权重
            if (wordcount.containsKey(s)){
                int count = wordcount.get(s);
                if (count > overcount){   //过滤超频词
                    continue;
                }
                wordcount.put(s,count+1);
            }else{
                wordcount.put(s,1);
            }
        }
        //计算每个词的hash
      for (String s:TermList){
          BigInteger t = this.hash(s);
          for (int i =0;i<this.hashbits;i++){
            BigInteger bitmask = new BigInteger("1").shiftLeft(i);
            int weight = wordcount.get(s); //获取分词的词性
            if (t.and(bitmask).signum()!=0){
                v[i] += weight; //对hash值进行加权
            }else {
                v[i] -= weight;
            }
          }
      }

      BigInteger fingerprint = new BigInteger("0");
      for (int i = 0;i< this.hashbits;i++){
          if(v[i] >= 0){
              fingerprint = fingerprint.add(new BigInteger("1").shiftLeft(i));  //对加权后的hash值降维
          }
      }

      return fingerprint;
    }

    private BigInteger hash(String s){
       if (s ==null||s.length()==0){
           return  new BigInteger("0");
       }else{
           //当source的长度过短，会导致hash算法失效，需要对过短的词进行补偿
           while (s.length()<3){
               s = s+s.charAt(0);
           }
           char[] sArray = s.toCharArray();
           BigInteger x = BigInteger.valueOf(((long)sArray[0])<<7);
           BigInteger m = new BigInteger("1000003");
           BigInteger mask = new BigInteger("2").pow(this.hashbits).subtract(new BigInteger("1"));
           for (char item:sArray){
               BigInteger temp = BigInteger.valueOf((long) item);
               x = x.multiply(m).xor(temp).and(mask);
           }
           x = x.xor(new BigInteger(String.valueOf(s.length())));
           if (x.equals(new BigInteger("-1"))){
               x = new BigInteger("-2");
           }
           return x;
       }
    }

    public int hammingDistance(simhash s2){
       BigInteger m = new BigInteger("1").shiftLeft(this.hashbits).subtract(new BigInteger("1"));
       BigInteger x = this.strSimHash.xor(s2.strSimHash).and(m);    //对两个文本的指纹进行异或处理
       int tot = 0;
       while (x.signum()!=0){
           tot += 1;
           x = x.and(x.subtract(new BigInteger("1")));  //求出汉明距离
       }
       return tot;
    }

    public  double getSemblance(simhash s2){
       double i = (double) this.hammingDistance(s2);
       return  1-i/this.hashbits;
    }

}
