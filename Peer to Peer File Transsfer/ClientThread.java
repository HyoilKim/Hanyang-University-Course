import java.io.*;
import java.net.Socket;
import java.util.Random;

class ClientThread extends Thread{
	// ************** Server ������� ���� chunk�� 3�� ���� �� �ڽ��� ���Ͽ� ����  ************* //
	// **************        ���� ������ FileManager��  �ǹ� ����                    ************* //
	int port;
	int peerNum;
	int ownNum;
	byte[] buffer;
	boolean isFirst;
	String ip;
	String bitMap;
	FileManager fileManager;
	final int BUFFER_SIZE = 10240;
		
	public ClientThread(FileManager fileManager) {
		this.fileManager = fileManager;
		this.buffer = new byte[10240];
	}

	public void run() {	
    	String filename = fileManager.getFilename();
    	String filePath = fileManager.getFilePath();
        File file = new File(filePath+filename);
        
		while(true) {
			fileManager.setConnectPeerNum();		// ������ ���� �� Peer����(������)
			ownNum = fileManager.getOwnNum();		// ���� PeerNum ����
	        ip = fileManager.getPeerIp();			// ���� Peer IP ����
	        port = fileManager.getPeerPort();		// ���� Peer port ����
	        fileManager.initNumOfDown();			// �ٿ�ε� Ƚ�� 3 ����
	        
	        try {
	    		// ************** ������ ����, ûũ ����&�ޱ� �غ�************* //
	        	Socket receiveSocket = new Socket(ip, port);		        
	        	System.out.println(fileManager.portArr[peerNum] + " client thread connect with " + port);
		      
		        InputStream is = receiveSocket.getInputStream();	
				OutputStream os = receiveSocket.getOutputStream();
				DataInputStream streamFromSender = new DataInputStream(is);
		        DataOutputStream streamToSender = new DataOutputStream(os);
		        RandomAccessFile raf = new RandomAccessFile(file, "rw");
		        String messageFromSender = "";
		        
				// ************** ����� Peer�� ������ �ִ��� Ȯ�� ************* //
		        if(streamFromSender.readUTF().equals("no file")) {
		        	Thread.sleep(1000);
		        	System.out.println(fileManager.portArr[ownNum] + " client thread quit with" + port);
		        	receiveSocket.close();
		        	continue;
		        }
		        
		        // ************** �ڽ��� ������ ���� ��� bitMap�ʱ�ȭ(���ο��� �̷�״� ��) ************* //
		        if (fileManager.getBitMap() == "") {
		        	streamToSender.writeUTF("want to chunkNum");
		        	Thread.sleep(1000);
		        	int chunkNum = Integer.parseInt(streamFromSender.readUTF());
		        	Thread.sleep(1000);
		        	fileManager.chunkNum = chunkNum;
					fileManager.initLeecherBitMap();
		        } else {
		        	streamToSender.writeUTF("don't want to chunkNum");
		        	Thread.sleep(1000);
		        	streamFromSender.readUTF();
		        }
		        
		        // ************** �ٸ� Peer�� ���� 3�� �ٿ�  ************* //
		        while(fileManager.getNumDown() < 3) {
		        	System.out.println("****** sending receiver's bitMap ******");
		        	// ************** �ٸ� Peer�� ���� �ʿ��� chunk�� �ִ��� Ȯ�� �� Get************* //
			        bitMap = fileManager.getBitMap();
		        	streamToSender.writeUTF(bitMap);
		        	Thread.sleep(1000);
		        	messageFromSender = streamFromSender.readUTF();
		        	
			        if (messageFromSender.equals("server thread have a chunk")) {
			        	System.out.println("****** sender has chunks ******");
			        	int missIndex = Integer.parseInt(streamFromSender.readUTF());	// ���� ������ ���� ���� chunk�� ���� bitMap�� index 
			        	streamToSender.flush();
			        	streamToSender.writeUTF("thank u missIndex");
			        	Thread.sleep(1000);    
			            
			        	int size = Integer.parseInt(streamFromSender.readUTF());		// ����� Peer�� ������ chunk�� ũ��
			        	streamToSender.writeUTF("thank u size");
			        	Thread.sleep(1000);
			        	
			            buffer = new byte[10240];
			        	streamFromSender.read(buffer);
			        	Thread.sleep(1000);
			            raf.seek(missIndex*BUFFER_SIZE);								// chunk ���� ��ġ ����

		        		FileOutputStream fos = new FileOutputStream(raf.getFD());		// chunk ���
		        		fos.write(buffer, 0, size);
		        		
			            fileManager.updateBitMap(missIndex);							// ������ ���� chunk�� �޾Ƽ� �� ���Ͽ� ����߱� ������ bitMap ����
				        fileManager.plusNumOfDown();
			        } else {
			        	if (fileManager.isChunkFull()) {								// chunk�� ���� á�ٸ� Seeder�� ����
				        	fileManager.isSeeder[fileManager.ownNum] = true;
					    }
			        	break;
			        }
		        }
		        // Seeder�� ��쿡 Thread����
		        if (fileManager.isSeeder()) {	
		        	System.out.println("All chunks download completed");
		        	receiveSocket.close();
		        	break;
			    }
	        	receiveSocket.close();
				raf.close();
		    } catch (FileNotFoundException e) {
				e.printStackTrace();
			}catch(Exception e){
				e.getStackTrace();
		    }
		}
	}
}