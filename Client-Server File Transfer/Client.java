import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FilterOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Scanner;

public class Client {
	public static void main(String[] args){
        String ip = args[0];
        int port = Integer.parseInt(args[1]);
                
        try{
            Socket clientSocket = new Socket(ip, port); 
            System.out.println("클라이언트 접속완료");
        
            InputStream is = clientSocket.getInputStream();	//서버에서 output data를 가져오는 스트림
            Scanner in = new Scanner(System.in);
            String filename = args[2];
            FileOutputStream fos = new FileOutputStream(filename);
            
            byte[] buffer = new byte[10000];       // 버퍼크기 설정 -10KB.
            int readBytes;
            while ((readBytes = is.read(buffer)) != -1) {	// 버퍼크기만큼 서버에서 받아온 data를 클라이언트 파일에 저장
            	fos.write(buffer, 0, readBytes);
            }    
            
            System.out.println("파일 다운로드 완료");
            
            clientSocket.close();
            is.close();
            in.close();
            fos.close();
        } catch(Exception e){
        	e.getStackTrace();
        }
    }
}
