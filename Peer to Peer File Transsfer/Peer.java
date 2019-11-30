import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;

public class Peer {	
	// ************** Client, Server�����带 ������ Peer ************* //
	static public int BUFFER_SIZE = 10240;
	public static void main(String args[]) throws IOException, InterruptedException {
		Scanner in = new Scanner(System.in);
		System.out.println("******** p2p ********");
		System.out.print("Peer num(0~4): ");
		int peerNum = Integer.parseInt(in.nextLine());
		System.out.print("filename: ");
		String filename = in.nextLine();
		
		FileManager fileManager = new FileManager(peerNum);
		fileManager.setFilename(filename);
		fileManager.setFilePath();
		
		File file = new File("configuration.txt");
		FileReader fr = new FileReader(file);
		BufferedReader br = new BufferedReader(fr);
		StringTokenizer st;

		int port = 0;
		String ip = "";
		
		// ************** configuration file�� ���� IP�� port�Է¹ޱ� ************* //
		for (int i = 0; i < 5; i++) {
			st = new StringTokenizer(br.readLine());
			ip = st.nextToken();
			port = Integer.parseInt(st.nextToken());
			
			fileManager.ipArr[i] = ip;
			fileManager.portArr[i] = port;		
		}

		// ************** Seeder�ʱ�ȭ(leecher�� seeder�� ������� �� �ʱ�ȭ) ************* //
		if(peerNum == 0) {
			fileManager.initSeederBitMap();
		}
		br.close();

		// ************** Client ������ ���� ************* //
		ClientThread receiveThread = new ClientThread(fileManager);
		receiveThread.start();

		// ************** Server������ ���� ************* //
		ServerSocket welcomeSocket = new ServerSocket(fileManager.portArr[peerNum]);
		while(true) {
			System.out.println(fileManager.portArr[peerNum]+ " server thread create");
			Socket connectSocket = welcomeSocket.accept();
			System.out.println(fileManager.portArr[peerNum] + " server thread connected");		
			ServerThread senderThread = new ServerThread(connectSocket, fileManager, peerNum);
			senderThread.start();
		}		
	}
}