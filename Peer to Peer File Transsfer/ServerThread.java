import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

class ServerThread extends Thread{
	// **************       자신의 파일을 연결된 Peer에게 전달하는 쓰레드              ************* //
	// **************        지역 변수는 FileManager와  의미 동일                    ************* //
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

	// ************** 연결된 피어에게 없는 chunk에 대한 Index 반환 ************* //
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
			// ************** Socket통신을 위한 준비  ************* //
			OutputStream os = connectSocket.getOutputStream();		
		    DataOutputStream streamToReceiver = new DataOutputStream(os);
			InputStream is = connectSocket.getInputStream();		
			DataInputStream streamFromReceiver = new DataInputStream(is);			
		    String messageFromReceiver;
		
			// ************** 나에 대한 정보 세팅 ************* //
			filename = fileManager.getFilename();
			filePath = fileManager.getFilePath();
			filename = filePath + filename;
			bitMap = fileManager.getBitMap();
			fileManager.initNumOfDown();
			String clientBitMap;

			// ************** 연결된 피어에게 줄 파일이 나에게 있는지 확인  ************* //
			File file = new File(filename);
			if(!file.exists()) {
		    	streamToReceiver.writeUTF("no file");
		    	file.delete();
		    	System.out.println("peer에게 전송할 파일이 없음");
		    	Thread.sleep(1);										//스레드 강제종료
		    } else {
		    	streamToReceiver.writeUTF("file exists");
		    }
			RandomAccessFile raf = new RandomAccessFile(filename, "rw");
			
			// ************** 연결 된 피어에게 chunkNum 전달 ************* //
			if(streamFromReceiver.readUTF().equals("want to chunkNum")) {
				streamToReceiver.writeUTF(fileManager.chunkNum+"");
			} else {
				streamToReceiver.writeUTF("null");
			}
			
			// ************** 연결 된 피어에게 chunk 전달 ************* //
			while (fileManager.getNumDown() < 3) {
				System.out.println("******getting client's bitMap*******");
				clientBitMap = streamFromReceiver.readUTF();
				int missIndex = findMissingIndex(clientBitMap);
				
				// ************** 연결 된 Peer에게 없고 나에게는 있는지 확인 ************* //
				if (missIndex == -1) {
					System.out.println(fileManager.portArr[peerNum] + " sender doesn't has a file Chunk");
					streamToReceiver.writeUTF("connect fail");
					break;
				}else {
					System.out.println(fileManager.portArr[peerNum] + " sender have a file Chunk");
					streamToReceiver.writeUTF("server thread have a chunk");
				}

				// ************** 전송할 파일 읽기 및 전송************* //
				buffer = new byte[BUFFER_SIZE];
				raf.seek(missIndex*BUFFER_SIZE);
				FileInputStream fis = new FileInputStream(raf.getFD());
				int size = fis.read(buffer, 0, buffer.length);
				
				streamToReceiver.writeUTF(missIndex+"");
				if (streamFromReceiver.readUTF().equals("thank u missIndex")) {
					System.out.println("miss index 전달완료");	
				}
				
				streamToReceiver.writeUTF(size+"");
				if(streamFromReceiver.readUTF().equals("thank u size")) {
					System.out.println("size 전달완료");
				}
				streamToReceiver.write(buffer, 0, size);
				
				System.out.println("one chunk trasnfer & update bitMap\n");
				fileManager.plusNumOfDown();
			}	
		    raf.close();
		    os.close();
			connectSocket.close();
		} catch(InterruptedException e) {
	    	System.out.println("센드 스레드 강제종료");
		} catch(IOException e) {
			 
		} 
		System.out.println(fileManager.portArr[peerNum] + " send Thread run 메소드 종료");
	}
}