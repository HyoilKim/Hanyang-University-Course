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
            System.out.println("Ŭ���̾�Ʈ ���ӿϷ�");
        
            InputStream is = clientSocket.getInputStream();	//�������� output data�� �������� ��Ʈ��
            Scanner in = new Scanner(System.in);
            String filename = args[2];
            FileOutputStream fos = new FileOutputStream(filename);
            
            byte[] buffer = new byte[10000];       // ����ũ�� ���� -10KB.
            int readBytes;
            while ((readBytes = is.read(buffer)) != -1) {	// ����ũ�⸸ŭ �������� �޾ƿ� data�� Ŭ���̾�Ʈ ���Ͽ� ����
            	fos.write(buffer, 0, readBytes);
            }    
            
            System.out.println("���� �ٿ�ε� �Ϸ�");
            
            clientSocket.close();
            is.close();
            in.close();
            fos.close();
        } catch(Exception e){
        	e.getStackTrace();
        }
    }
}
