import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

class ServerThread extends Thread{
	// **************       �ڽ��� ������ ����� Peer���� �����ϴ� ������              ************* //
	// **************        ���� ������ FileManager��  �ǹ� ����                    ************* //
	int peerNum;
	int port;
	final int BUFFER_SIZE = 10240;
	byte[] buffer; 	   
	String bitMap;
	String filename;
	String filePath;
	Socket connectSocket;  
	FileManager fileManager;
	
	ServerThread(Socket connectSokcet, FileManager fileManager, int peerNum){
		this.connectSocket = connectSokcet;
		this.peerNum = peerNum;
		this.fileManager = fileManager;
		buffer = new byte[BUFFER_SIZE];
	}

	// ************** ����� �Ǿ�� ���� chunk�� ���� Index ��ȯ ************* //
	public int findMissingIndex(String clientBitMap) {
		for (int i = 0; i < bitMap.length(); i++) {
			if (this.bitMap.charAt(i) == '1' && clientBitMap.charAt(i) == '0') {
				return i;
			}
		}
		return -1;
	}
	
	public synchronized void run() {   
		try {
			// ************** Socket����� ���� �غ�  ************* //
			OutputStream os = connectSocket.getOutputStream();		
		    DataOutputStream streamToReceiver = new DataOutputStream(os);
			InputStream is = connectSocket.getInputStream();		
			DataInputStream streamFromReceiver = new DataInputStream(is);			
		    String messageFromReceiver;
		
			// ************** ���� ���� ���� ���� ************* //
			filename = fileManager.getFilename();
			filePath = fileManager.getFilePath();
			filename = filePath + filename;
			bitMap = fileManager.getBitMap();
			fileManager.initNumOfDown();
			String clientBitMap;

			// ************** ����� �Ǿ�� �� ������ ������ �ִ��� Ȯ��  ************* //
			File file = new File(filename);
			if(!file.exists()) {
		    	streamToReceiver.writeUTF("no file");
		    	file.delete();
		    	System.out.println("peer���� ������ ������ ����");
		    	Thread.sleep(1);										//������ ��������
		    } else {
		    	streamToReceiver.writeUTF("file exists");
		    }
			RandomAccessFile raf = new RandomAccessFile(filename, "rw");
			
			// ************** ���� �� �Ǿ�� chunkNum ���� ************* //
			if(streamFromReceiver.readUTF().equals("want to chunkNum")) {
				streamToReceiver.writeUTF(fileManager.chunkNum+"");
			} else {
				streamToReceiver.writeUTF("null");
			}
			
			// ************** ���� �� �Ǿ�� chunk ���� ************* //
			while (fileManager.getNumDown() < 3) {
				System.out.println("******getting client's bitMap*******");
				clientBitMap = streamFromReceiver.readUTF();
				int missIndex = findMissingIndex(clientBitMap);
				
				// ************** ���� �� Peer���� ���� �����Դ� �ִ��� Ȯ�� ************* //
				if (missIndex == -1) {
					System.out.println(fileManager.portArr[peerNum] + " sender doesn't has a file Chunk");
					streamToReceiver.writeUTF("connect fail");
					break;
				}else {
					System.out.println(fileManager.portArr[peerNum] + " sender have a file Chunk");
					streamToReceiver.writeUTF("server thread have a chunk");
				}

				// ************** ������ ���� �б� �� ����************* //
				buffer = new byte[BUFFER_SIZE];
				raf.seek(missIndex*BUFFER_SIZE);
				FileInputStream fis = new FileInputStream(raf.getFD());
				int size = fis.read(buffer, 0, buffer.length);
				
				streamToReceiver.writeUTF(missIndex+"");
				if (streamFromReceiver.readUTF().equals("thank u missIndex")) {
					System.out.println("miss index ���޿Ϸ�");	
				}
				
				streamToReceiver.writeUTF(size+"");
				if(streamFromReceiver.readUTF().equals("thank u size")) {
					System.out.println("size ���޿Ϸ�");
				}
				streamToReceiver.write(buffer, 0, size);
				
				System.out.println("one chunk trasnfer & update bitMap\n");
				fileManager.plusNumOfDown();
			}	
		    raf.close();
		    os.close();
			connectSocket.close();
		} catch(InterruptedException e) {
	    	System.out.println("���� ������ ��������");
		} catch(IOException e) {
			 
		} 
		System.out.println(fileManager.portArr[peerNum] + " send Thread run �޼ҵ� ����");
	}
}