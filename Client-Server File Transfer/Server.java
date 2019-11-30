import java.io.*;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Server  {  
    public static void main(String[] args) throws Exception{
    	int port = Integer.parseInt(args[0]);
    	try {
	    	ServerSocket serverSocket = new ServerSocket(port);  // 소켓 생성
	        System.out.println("서버준비 완료");
	        
	        Socket clientSocket = serverSocket.accept();   // 클라이언트 접속 대기
	        System.out.println("소켓준비 완료");
	        
	        OutputStream os = clientSocket.getOutputStream();	// 클라이언트에게 파일을 전송해주는 스트림
	        
        	String filename = args[1];		       
        	FileInputStream fis = new FileInputStream(filename);
	        
	        byte[] buffer = new byte[10000]; // 버퍼크기 설정 - 10KB
	        int readBytes;
	        while((readBytes = fis.read(buffer)) > 0) {		// 버퍼 크기만큼 서버의 파일을 읽어서 클라이언트에게 전송
	        	os.write(buffer, 0, readBytes);
	        }
	        
	        System.out.println("파일전송완료");
	        System.out.println("서버종료");
	        
	        fis.close();
	        serverSocket.close();
	        os.close();
        } catch(Exception e) {
        	e.getStackTrace();
        }
    }
}
