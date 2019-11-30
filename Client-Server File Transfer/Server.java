import java.io.*;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Server  {  
    public static void main(String[] args) throws Exception{
    	int port = Integer.parseInt(args[0]);
    	try {
	    	ServerSocket serverSocket = new ServerSocket(port);  // ���� ����
	        System.out.println("�����غ� �Ϸ�");
	        
	        Socket clientSocket = serverSocket.accept();   // Ŭ���̾�Ʈ ���� ���
	        System.out.println("�����غ� �Ϸ�");
	        
	        OutputStream os = clientSocket.getOutputStream();	// Ŭ���̾�Ʈ���� ������ �������ִ� ��Ʈ��
	        
        	String filename = args[1];		       
        	FileInputStream fis = new FileInputStream(filename);
	        
	        byte[] buffer = new byte[10000]; // ����ũ�� ���� - 10KB
	        int readBytes;
	        while((readBytes = fis.read(buffer)) > 0) {		// ���� ũ�⸸ŭ ������ ������ �о Ŭ���̾�Ʈ���� ����
	        	os.write(buffer, 0, readBytes);
	        }
	        
	        System.out.println("�������ۿϷ�");
	        System.out.println("��������");
	        
	        fis.close();
	        serverSocket.close();
	        os.close();
        } catch(Exception e) {
        	e.getStackTrace();
        }
    }
}
